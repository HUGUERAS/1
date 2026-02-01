# 💳 Modelo Pay As You Go - Ativo Real

## 📋 Visão Geral

Este documento descreve a implementação de um modelo de **assinatura recorrente** (Pay As You Go) para o sistema Ativo Real, permitindo diferentes planos de acesso com limites e funcionalidades específicas.

## 🎯 Objetivos

1. **Monetização Recorrente**: Criar fluxo de receita previsível através de assinaturas mensais
2. **Escalabilidade**: Permitir que topógrafos escolham planos adequados ao seu volume de trabalho
3. **Flexibilidade**: Possibilitar upgrade/downgrade de planos conforme necessidade
4. **Automação**: Renovação automática de assinaturas via webhook

---

## 🏗️ Arquitetura do Modelo

### Componentes Principais

```
┌─────────────────────┐
│  Planos Disponíveis │
│  (PlanoPagamento)   │
└──────────┬──────────┘
           │ 1:N
           │
┌──────────▼──────────┐
│    Assinaturas      │
│    (Assinatura)     │
└──────────┬──────────┘
           │ N:1
           │
┌──────────▼──────────┐
│     Topógrafo       │
│     (Usuario)       │
└─────────────────────┘
```

### Fluxo de Negócio

```
1. Topógrafo se registra → Plano FREE (trial 30 dias)
2. Escolhe plano pago → Cria assinatura PENDENTE
3. Realiza pagamento → Assinatura ATIVA
4. Usa o sistema dentro dos limites do plano
5. Renovação automática (webhook) → Nova cobrança
6. Cancelamento/Expiração → Downgrade para FREE
```

---

## 📊 Estrutura de Planos

### Planos Oferecidos

| Plano | Preço/Mês | Projetos | Lotes/Projeto | Armazenamento | Suporte |
|-------|-----------|----------|---------------|---------------|---------|
| **FREE** | R$ 0 | 2 | 10 | 100 MB | Email |
| **BÁSICO** | R$ 99 | 10 | 50 | 1 GB | Email + Chat |
| **PROFISSIONAL** | R$ 299 | 50 | 200 | 10 GB | Email + Chat + Telefone |
| **ENTERPRISE** | R$ 999 | Ilimitado | Ilimitado | 100 GB | Dedicado + WhatsApp |

### Funcionalidades por Plano

```python
LIMITES_PLANO = {
    "FREE": {
        "max_projetos": 2,
        "max_lotes_por_projeto": 10,
        "storage_mb": 100,
        "export_formato": ["PDF"],
        "api_rate_limit": 100,  # requests/hora
    },
    "BASICO": {
        "max_projetos": 10,
        "max_lotes_por_projeto": 50,
        "storage_mb": 1024,
        "export_formato": ["PDF", "KML"],
        "api_rate_limit": 500,
    },
    "PROFISSIONAL": {
        "max_projetos": 50,
        "max_lotes_por_projeto": 200,
        "storage_mb": 10240,
        "export_formato": ["PDF", "KML", "SHP", "DXF"],
        "api_rate_limit": 2000,
    },
    "ENTERPRISE": {
        "max_projetos": -1,  # Ilimitado
        "max_lotes_por_projeto": -1,
        "storage_mb": 102400,
        "export_formato": ["PDF", "KML", "SHP", "DXF", "GeoJSON"],
        "api_rate_limit": -1,  # Sem limite
    }
}
```

---

## 🗄️ Modelo de Dados

### 1. Tabela `planos_pagamento`

```sql
CREATE TABLE planos_pagamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,  -- FREE, BASICO, PROFISSIONAL, ENTERPRISE
    descricao TEXT,
    preco_mensal NUMERIC(10, 2) NOT NULL,
    
    -- Limites
    max_projetos INTEGER DEFAULT -1,  -- -1 = ilimitado
    max_lotes_por_projeto INTEGER DEFAULT -1,
    storage_mb INTEGER DEFAULT 100,
    
    -- Recursos
    permite_export_kml BOOLEAN DEFAULT FALSE,
    permite_export_shp BOOLEAN DEFAULT FALSE,
    permite_export_dxf BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    features JSONB,  -- {"api_access": true, "priority_support": false}
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Tabela `assinaturas`

```sql
CREATE TYPE status_assinatura AS ENUM (
    'TRIAL',           -- Trial gratuito (30 dias)
    'PENDENTE',        -- Aguardando pagamento
    'ATIVA',           -- Assinatura ativa
    'CANCELADA',       -- Cancelada pelo usuário
    'SUSPENSA',        -- Suspensa por falta de pagamento
    'EXPIRADA'         -- Trial/assinatura expirada
);

CREATE TABLE assinaturas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),  -- Topógrafo
    plano_id INTEGER REFERENCES planos_pagamento(id),
    
    -- Status
    status status_assinatura NOT NULL DEFAULT 'TRIAL',
    
    -- Datas
    inicio_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expira_em TIMESTAMP,  -- Data de expiração do período atual
    cancelada_em TIMESTAMP,
    proximo_pagamento TIMESTAMP,  -- Próxima cobrança programada
    
    -- Pagamento
    gateway_subscription_id VARCHAR(100),  -- ID na InfinitePay/Stripe
    metodo_pagamento VARCHAR(20),  -- PIX, CARTAO, BOLETO
    
    -- Auditoria
    metadata JSONB,  -- Histórico de upgrades, downgrades
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_assinaturas_usuario ON assinaturas(usuario_id);
CREATE INDEX idx_assinaturas_status ON assinaturas(status);
CREATE INDEX idx_assinaturas_expira ON assinaturas(expira_em);
```

### 3. Tabela `historico_assinaturas`

```sql
CREATE TABLE historico_assinaturas (
    id SERIAL PRIMARY KEY,
    assinatura_id INTEGER REFERENCES assinaturas(id),
    acao VARCHAR(50),  -- 'CRIADA', 'RENOVADA', 'UPGRADE', 'DOWNGRADE', 'CANCELADA'
    plano_anterior VARCHAR(50),
    plano_novo VARCHAR(50),
    valor_pago NUMERIC(10, 2),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔧 Implementação Backend

### Schemas Pydantic (`schemas.py`)

```python
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class StatusAssinatura(str, Enum):
    TRIAL = "TRIAL"
    PENDENTE = "PENDENTE"
    ATIVA = "ATIVA"
    CANCELADA = "CANCELADA"
    SUSPENSA = "SUSPENSA"
    EXPIRADA = "EXPIRADA"

class PlanoBase(BaseModel):
    nome: str
    descricao: Optional[str]
    preco_mensal: float
    max_projetos: int
    max_lotes_por_projeto: int
    storage_mb: int
    permite_export_kml: bool = False
    permite_export_shp: bool = False
    permite_export_dxf: bool = False

class PlanoResponse(PlanoBase):
    id: int
    features: Optional[Dict[str, Any]]
    ativo: bool
    
    class Config:
        from_attributes = True

class AssinaturaCreate(BaseModel):
    plano_id: int
    metodo_pagamento: str  # PIX, CARTAO, BOLETO

class AssinaturaResponse(BaseModel):
    id: int
    usuario_id: int
    plano_id: int
    status: StatusAssinatura
    inicio_em: datetime
    expira_em: Optional[datetime]
    proximo_pagamento: Optional[datetime]
    
    class Config:
        from_attributes = True
```

### Models SQLAlchemy (`models.py`)

```python
from sqlalchemy import Column, Integer, String, Numeric, Boolean, TIMESTAMP, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
import enum

class StatusAssinaturaEnum(enum.Enum):
    TRIAL = "TRIAL"
    PENDENTE = "PENDENTE"
    ATIVA = "ATIVA"
    CANCELADA = "CANCELADA"
    SUSPENSA = "SUSPENSA"
    EXPIRADA = "EXPIRADA"

class PlanoPagamento(Base):
    __tablename__ = "planos_pagamento"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, nullable=False)
    descricao = Column(String)
    preco_mensal = Column(Numeric(10, 2), nullable=False)
    
    # Limites
    max_projetos = Column(Integer, default=-1)
    max_lotes_por_projeto = Column(Integer, default=-1)
    storage_mb = Column(Integer, default=100)
    
    # Recursos
    permite_export_kml = Column(Boolean, default=False)
    permite_export_shp = Column(Boolean, default=False)
    permite_export_dxf = Column(Boolean, default=False)
    
    # Metadata
    features = Column(JSON)
    ativo = Column(Boolean, default=True)
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    
    # Relationships
    assinaturas = relationship("Assinatura", back_populates="plano")

class Assinatura(Base):
    __tablename__ = "assinaturas"
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    plano_id = Column(Integer, ForeignKey("planos_pagamento.id"))
    
    status = Column(Enum(StatusAssinaturaEnum), default=StatusAssinaturaEnum.TRIAL)
    
    inicio_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    expira_em = Column(TIMESTAMP)
    cancelada_em = Column(TIMESTAMP)
    proximo_pagamento = Column(TIMESTAMP)
    
    gateway_subscription_id = Column(String(100))
    metodo_pagamento = Column(String(20))
    
    metadata = Column(JSON)
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    atualizado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    
    # Relationships
    plano = relationship("PlanoPagamento", back_populates="assinaturas")
```

---

## 🌐 API Endpoints

### 1. Listar Planos Disponíveis

```http
GET /api/planos
```

**Response:**
```json
[
  {
    "id": 1,
    "nome": "BASICO",
    "descricao": "Ideal para pequenos topógrafos",
    "preco_mensal": 99.00,
    "max_projetos": 10,
    "max_lotes_por_projeto": 50,
    "storage_mb": 1024,
    "permite_export_kml": true
  }
]
```

### 2. Criar Assinatura

```http
POST /api/assinaturas
Content-Type: application/json

{
  "plano_id": 2,
  "metodo_pagamento": "PIX"
}
```

**Response:**
```json
{
  "id": 1,
  "usuario_id": 123,
  "plano_id": 2,
  "status": "PENDENTE",
  "payment_url": "https://checkout.infinitepay.io/xyz123",
  "pix_qrcode": "data:image/png;base64,..."
}
```

### 3. Consultar Assinatura Atual

```http
GET /api/assinaturas/current
```

**Response:**
```json
{
  "id": 1,
  "plano": {
    "nome": "PROFISSIONAL",
    "preco_mensal": 299.00
  },
  "status": "ATIVA",
  "expira_em": "2026-02-28T23:59:59Z",
  "proximo_pagamento": "2026-02-28T00:00:00Z",
  "limites": {
    "projetos_usados": 15,
    "projetos_limite": 50,
    "storage_usado_mb": 450,
    "storage_limite_mb": 10240
  }
}
```

### 4. Cancelar Assinatura

```http
POST /api/assinaturas/{id}/cancelar
```

**Response:**
```json
{
  "message": "Assinatura cancelada com sucesso",
  "expira_em": "2026-02-28T23:59:59Z",
  "plano_futuro": "FREE"
}
```

### 5. Fazer Upgrade/Downgrade

```http
POST /api/assinaturas/{id}/alterar-plano
Content-Type: application/json

{
  "novo_plano_id": 3
}
```

---

## 🔄 Integração com Gateway

### InfinitePay - Assinaturas Recorrentes

```python
def criar_assinatura_recorrente(assinatura_id, plano, metodo_pagamento):
    """
    Cria uma assinatura recorrente no InfinitePay
    """
    payload = {
        "plan_id": f"ativo-real-{plano.nome.lower()}",
        "customer": {
            "email": usuario.email,
            "name": usuario.nome
        },
        "payment_method": metodo_pagamento,
        "billing_cycle": "monthly",
        "amount": int(plano.preco_mensal * 100),  # centavos
        "metadata": {
            "assinatura_id": str(assinatura_id),
            "usuario_id": str(usuario.id)
        },
        "webhook_url": f"{FUNCTION_APP_URL}/api/assinaturas/webhook"
    }
    
    response = requests.post(
        f"{INFINITEPAY_BASE_URL}/subscriptions",
        json=payload,
        headers={"Authorization": f"Bearer {INFINITEPAY_API_KEY}"}
    )
    
    return response.json()
```

### Webhook para Renovações

```python
@app.route(route="assinaturas/webhook", methods=["POST"])
def subscription_webhook(req: func.HttpRequest):
    """
    Recebe notificações de renovação, cancelamento, falha de pagamento
    """
    data = req.get_json()
    event_type = data.get("event")
    subscription_data = data.get("data")
    
    assinatura_id = subscription_data["metadata"]["assinatura_id"]
    
    if event_type == "subscription.renewed":
        # Renovação bem-sucedida
        atualizar_status_assinatura(assinatura_id, "ATIVA")
        estender_expiracao(assinatura_id, days=30)
        
    elif event_type == "subscription.payment_failed":
        # Falha no pagamento
        atualizar_status_assinatura(assinatura_id, "SUSPENSA")
        enviar_email_cobranca_falhou(assinatura_id)
        
    elif event_type == "subscription.cancelled":
        # Cancelamento
        atualizar_status_assinatura(assinatura_id, "CANCELADA")
```

---

## ✅ Validação de Limites

### Middleware de Validação

```python
def verificar_limite_plano(usuario_id: int, recurso: str):
    """
    Verifica se o usuário está dentro dos limites do plano
    """
    assinatura = db.query(Assinatura).filter(
        Assinatura.usuario_id == usuario_id,
        Assinatura.status == "ATIVA"
    ).first()
    
    if not assinatura:
        raise PermissionError("Nenhuma assinatura ativa")
    
    plano = assinatura.plano
    
    if recurso == "criar_projeto":
        count = db.query(Projeto).filter(Projeto.usuario_id == usuario_id).count()
        if plano.max_projetos != -1 and count >= plano.max_projetos:
            raise LimiteExcedidoError(
                f"Limite de {plano.max_projetos} projetos atingido. "
                f"Faça upgrade para criar mais projetos."
            )
```

### Exemplo de Uso na API

```python
@app.route(route="projetos", methods=["POST"])
def create_projeto(req: func.HttpRequest):
    usuario_id = req.headers.get("X-User-Id")
    
    # Validar limite ANTES de criar
    verificar_limite_plano(usuario_id, "criar_projeto")
    
    # Prosseguir com criação...
```

---

## 📱 Experiência do Usuário

### Fluxo de Onboarding

1. **Cadastro**: Novo usuário recebe 30 dias de trial no plano BÁSICO
2. **Exploração**: Usa o sistema sem restrições por 30 dias
3. **Notificação**: Recebe email 7 dias antes do fim do trial
4. **Escolha**: Seleciona plano ou downgrade automático para FREE
5. **Pagamento**: Realiza primeira cobrança
6. **Ativação**: Assinatura ativa imediatamente

### Notificações Importantes

```python
NOTIFICACOES = {
    "trial_7_dias": "Seu trial expira em 7 dias. Escolha um plano!",
    "trial_1_dia": "Último dia de trial! Não perca acesso às funcionalidades.",
    "pagamento_sucesso": "Pagamento confirmado! Assinatura renovada até {data}.",
    "pagamento_falha": "Falha no pagamento. Atualize seu método de pagamento.",
    "limite_80": "Você usou 80% do limite de projetos. Considere upgrade.",
    "cancelamento": "Assinatura cancelada. Acesso até {data}."
}
```

---

## 🎨 Interface (Componentes Sugeridos)

### 1. Tela de Planos

```tsx
// PricingPage.tsx
const PricingPage = () => {
  const plans = usePlans();
  
  return (
    <div className="grid grid-cols-4 gap-4">
      {plans.map(plan => (
        <PlanCard 
          key={plan.id}
          name={plan.nome}
          price={plan.preco_mensal}
          features={plan.features}
          onSelect={() => createSubscription(plan.id)}
        />
      ))}
    </div>
  );
};
```

### 2. Indicador de Uso

```tsx
// UsageBadge.tsx
const UsageBadge = ({ current, limit }) => {
  const percentage = (current / limit) * 100;
  const color = percentage > 80 ? 'red' : percentage > 50 ? 'yellow' : 'green';
  
  return (
    <div className="usage-badge">
      <span>{current} / {limit} projetos</span>
      <ProgressBar value={percentage} color={color} />
    </div>
  );
};
```

---

## 🧪 Testes

### Cenários de Teste

```python
def test_criar_assinatura_trial():
    """Novo usuário deve receber trial de 30 dias"""
    usuario = criar_usuario_teste()
    assinatura = criar_assinatura_trial(usuario.id)
    
    assert assinatura.status == "TRIAL"
    assert assinatura.expira_em == datetime.now() + timedelta(days=30)

def test_limite_plano_basico():
    """Plano básico deve limitar em 10 projetos"""
    usuario = criar_usuario_com_plano("BASICO")
    
    # Cria 10 projetos - OK
    for i in range(10):
        criar_projeto(usuario.id)
    
    # 11º projeto - ERRO
    with pytest.raises(LimiteExcedidoError):
        criar_projeto(usuario.id)

def test_renovacao_automatica():
    """Renovação deve estender assinatura por 30 dias"""
    assinatura = criar_assinatura_ativa()
    expira_antes = assinatura.expira_em
    
    renovar_assinatura(assinatura.id)
    
    assinatura.refresh()
    assert assinatura.expira_em == expira_antes + timedelta(days=30)
```

---

## 📈 Métricas Importantes

### KPIs a Acompanhar

```sql
-- MRR (Monthly Recurring Revenue)
SELECT 
    SUM(p.preco_mensal) as mrr
FROM assinaturas a
JOIN planos_pagamento p ON a.plano_id = p.id
WHERE a.status = 'ATIVA';

-- Taxa de Conversão Trial → Pago
SELECT 
    COUNT(CASE WHEN status IN ('ATIVA') THEN 1 END) * 100.0 / 
    COUNT(CASE WHEN status = 'TRIAL' THEN 1 END) as taxa_conversao
FROM assinaturas;

-- Churn Rate (Cancelamentos)
SELECT 
    COUNT(*) * 100.0 / 
    (SELECT COUNT(*) FROM assinaturas WHERE status = 'ATIVA') as churn_mensal
FROM assinaturas
WHERE cancelada_em >= DATE_TRUNC('month', CURRENT_DATE);
```

---

## 🚀 Próximos Passos

1. ✅ Implementar modelos de dados
2. ✅ Criar endpoints de API
3. ⏳ Integrar com InfinitePay Subscriptions
4. ⏳ Desenvolver interface de seleção de planos
5. ⏳ Implementar sistema de notificações
6. ⏳ Criar dashboard de métricas para admin
7. ⏳ Testes de integração completos

---

## 📚 Referências

- [InfinitePay Subscriptions API](https://docs.infinitepay.io/subscriptions)
- [Stripe Billing Best Practices](https://stripe.com/docs/billing/subscriptions/overview)
- [SaaS Metrics Guide](https://www.saasmetrics.co/)

---

**Última atualização:** 31/01/2026  
**Autor:** GitHub Copilot  
**Status:** 📝 Documentação Completa
