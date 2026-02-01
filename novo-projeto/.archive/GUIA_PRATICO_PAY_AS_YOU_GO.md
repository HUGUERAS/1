# 🚀 Guia Prático: Como Usar o Modelo Pay As You Go

Este guia mostra exemplos práticos de como usar o novo sistema de assinaturas no Ativo Real.

## 📝 Índice

1. [Listar Planos Disponíveis](#1-listar-planos-disponíveis)
2. [Criar Nova Assinatura](#2-criar-nova-assinatura)
3. [Consultar Assinatura Atual](#3-consultar-assinatura-atual)
4. [Fazer Upgrade de Plano](#4-fazer-upgrade-de-plano)
5. [Cancelar Assinatura](#5-cancelar-assinatura)
6. [Renovar Assinatura (Webhook)](#6-renovar-assinatura-webhook)
7. [Validar Limites do Plano](#7-validar-limites-do-plano)
8. [Exemplos Frontend](#8-exemplos-frontend)

---

## 1. Listar Planos Disponíveis

### Request

```bash
curl -X GET https://sua-api.azurewebsites.net/api/planos
```

### Response

```json
[
  {
    "id": 1,
    "nome": "FREE",
    "descricao": "Plano gratuito para teste",
    "preco_mensal": 0.00,
    "max_projetos": 2,
    "max_lotes_por_projeto": 10,
    "storage_mb": 100,
    "permite_export_kml": false,
    "permite_export_shp": false,
    "permite_export_dxf": false,
    "permite_api_access": false,
    "features": {
      "api_rate_limit": 100,
      "export_formats": ["PDF"],
      "support": "email"
    },
    "ativo": true,
    "ordem_exibicao": 1
  },
  {
    "id": 2,
    "nome": "BASICO",
    "descricao": "Ideal para pequenos topógrafos",
    "preco_mensal": 99.00,
    "max_projetos": 10,
    "max_lotes_por_projeto": 50,
    "storage_mb": 1024,
    "permite_export_kml": true,
    "permite_export_shp": false,
    "permite_export_dxf": false,
    "permite_api_access": false,
    "features": {
      "api_rate_limit": 500,
      "export_formats": ["PDF", "KML"],
      "support": "email+chat"
    },
    "ativo": true,
    "ordem_exibicao": 2
  },
  {
    "id": 3,
    "nome": "PROFISSIONAL",
    "descricao": "Para topógrafos profissionais",
    "preco_mensal": 299.00,
    "max_projetos": 50,
    "max_lotes_por_projeto": 200,
    "storage_mb": 10240,
    "permite_export_kml": true,
    "permite_export_shp": true,
    "permite_export_dxf": true,
    "permite_api_access": false,
    "features": {
      "api_rate_limit": 2000,
      "export_formats": ["PDF", "KML", "SHP", "DXF"],
      "support": "email+chat+phone"
    },
    "ativo": true,
    "ordem_exibicao": 3
  }
]
```

---

## 2. Criar Nova Assinatura

### Request

```bash
curl -X POST https://sua-api.azurewebsites.net/api/assinaturas \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 123,
    "plano_id": 2,
    "metodo_pagamento": "PIX"
  }'
```

### Response (Sucesso)

```json
{
  "id": 1,
  "usuario_id": 123,
  "plano_id": 2,
  "status": "PENDENTE",
  "inicio_em": "2026-01-31T10:00:00Z",
  "expira_em": null,
  "proximo_pagamento": "2026-01-31T10:00:00Z",
  "gateway_subscription_id": null,
  "metodo_pagamento": "PIX"
}
```

### Response (Erro - Já tem assinatura)

```json
{
  "error": "Usuário já possui assinatura ativa (ID: 1)"
}
```

---

## 3. Consultar Assinatura Atual

### Request

```bash
curl -X GET "https://sua-api.azurewebsites.net/api/assinaturas/current?usuario_id=123"
```

### Response

```json
{
  "id": 1,
  "usuario_id": 123,
  "status": "ATIVA",
  "inicio_em": "2026-01-15T10:00:00Z",
  "expira_em": "2026-02-15T10:00:00Z",
  "proximo_pagamento": "2026-02-15T00:00:00Z",
  "dias_restantes": 15,
  "plano": {
    "id": 2,
    "nome": "BASICO",
    "preco_mensal": 99.00,
    "max_projetos": 10,
    "max_lotes_por_projeto": 50,
    "storage_mb": 1024
  }
}
```

---

## 4. Fazer Upgrade de Plano

### Request

```bash
curl -X POST https://sua-api.azurewebsites.net/api/assinaturas/1/alterar-plano \
  -H "Content-Type: application/json" \
  -d '{
    "novo_plano_id": 3
  }'
```

### Response

```json
{
  "message": "Plano alterado com sucesso",
  "assinatura_id": 1,
  "novo_plano": {
    "id": 3,
    "nome": "PROFISSIONAL",
    "preco_mensal": 299.00
  }
}
```

---

## 5. Cancelar Assinatura

### Request

```bash
curl -X POST https://sua-api.azurewebsites.net/api/assinaturas/1/cancelar
```

### Response

```json
{
  "message": "Assinatura cancelada com sucesso",
  "assinatura_id": 1,
  "expira_em": "2026-02-15T10:00:00Z",
  "status": "CANCELADA"
}
```

**Nota:** A assinatura permanece ativa até a data de expiração.

---

## 6. Renovar Assinatura (Webhook)

Este endpoint é chamado automaticamente pelo gateway de pagamento quando uma renovação é bem-sucedida.

### Request

```bash
curl -X POST https://sua-api.azurewebsites.net/api/assinaturas/1/renovar \
  -H "Content-Type: application/json" \
  -d '{
    "gateway_payment_id": "pay_abc123xyz"
  }'
```

### Response

```json
{
  "message": "Assinatura renovada com sucesso",
  "assinatura_id": 1,
  "expira_em": "2026-03-15T10:00:00Z",
  "proximo_pagamento": "2026-03-15T00:00:00Z"
}
```

---

## 7. Validar Limites do Plano

### Exemplo em Python (Backend)

```python
from logic_services import verificar_limite_plano

def criar_projeto_com_validacao(usuario_id: int, projeto_data: dict, db: Session):
    """
    Cria projeto validando limites do plano
    """
    # Validar se pode criar mais projetos
    pode_criar = verificar_limite_plano(usuario_id, "projetos", db)
    
    if not pode_criar:
        raise ValueError(
            "Limite de projetos atingido. "
            "Faça upgrade do seu plano para criar mais projetos."
        )
    
    # Prosseguir com criação do projeto
    novo_projeto = Projeto(**projeto_data)
    db.add(novo_projeto)
    db.commit()
    
    return novo_projeto
```

### Exemplo de Validação na API

```python
@app.route(route="projetos", methods=["POST"])
def create_projeto_validado(req: func.HttpRequest) -> func.HttpResponse:
    usuario_id = req.headers.get("X-User-Id")  # Assume autenticação
    
    db = SessionLocal()
    try:
        # Validar limite ANTES de criar
        if not logic_services.verificar_limite_plano(int(usuario_id), "projetos", db):
            assinatura = logic_services.obter_assinatura_atual(int(usuario_id), db)
            return func.HttpResponse(
                body=json.dumps({
                    "error": "Limite de projetos atingido",
                    "plano_atual": assinatura.plano.nome,
                    "limite": assinatura.plano.max_projetos,
                    "sugestao": "Faça upgrade para criar mais projetos"
                }),
                status_code=403,
                mimetype="application/json"
            )
        
        # Criar projeto normalmente...
        
    finally:
        db.close()
```

---

## 8. Exemplos Frontend

### 8.1 Componente de Seleção de Planos (React)

```tsx
// PricingPlans.tsx
import React, { useEffect, useState } from 'react';

interface Plan {
  id: number;
  nome: string;
  descricao: string;
  preco_mensal: number;
  max_projetos: number;
  max_lotes_por_projeto: number;
  features: {
    export_formats: string[];
    support: string;
  };
}

export const PricingPlans: React.FC = () => {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/planos')
      .then(res => res.json())
      .then(data => {
        setPlans(data);
        setLoading(false);
      });
  }, []);

  const handleSelectPlan = async (planId: number) => {
    const response = await fetch('/api/assinaturas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        usuario_id: getCurrentUserId(),  // Função fictícia
        plano_id: planId,
        metodo_pagamento: 'PIX'
      })
    });

    if (response.ok) {
      alert('Assinatura criada! Redirecionando para pagamento...');
      // Redirecionar para checkout
    }
  };

  if (loading) return <div>Carregando planos...</div>;

  return (
    <div className="grid grid-cols-4 gap-6">
      {plans.map(plan => (
        <div key={plan.id} className="border rounded-lg p-6">
          <h3 className="text-xl font-bold">{plan.nome}</h3>
          <p className="text-gray-600">{plan.descricao}</p>
          <div className="text-3xl font-bold my-4">
            R$ {plan.preco_mensal.toFixed(2)}/mês
          </div>
          
          <ul className="space-y-2 mb-6">
            <li>✓ {plan.max_projetos === -1 ? 'Ilimitado' : plan.max_projetos} projetos</li>
            <li>✓ {plan.max_lotes_por_projeto === -1 ? 'Ilimitado' : plan.max_lotes_por_projeto} lotes/projeto</li>
            <li>✓ Exportar: {plan.features.export_formats.join(', ')}</li>
            <li>✓ Suporte: {plan.features.support}</li>
          </ul>
          
          <button 
            onClick={() => handleSelectPlan(plan.id)}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Escolher Plano
          </button>
        </div>
      ))}
    </div>
  );
};
```

### 8.2 Indicador de Uso (React)

```tsx
// UsageBadge.tsx
import React, { useEffect, useState } from 'react';

interface CurrentSubscription {
  plano: {
    nome: string;
    max_projetos: number;
  };
  dias_restantes: number;
}

export const UsageBadge: React.FC<{ userId: number }> = ({ userId }) => {
  const [subscription, setSubscription] = useState<CurrentSubscription | null>(null);
  const [projectsCount, setProjectsCount] = useState(0);

  useEffect(() => {
    // Buscar assinatura atual
    fetch(`/api/assinaturas/current?usuario_id=${userId}`)
      .then(res => res.json())
      .then(data => setSubscription(data));

    // Buscar quantidade de projetos
    fetch(`/api/projetos?usuario_id=${userId}`)
      .then(res => res.json())
      .then(data => setProjectsCount(data.length));
  }, [userId]);

  if (!subscription) return null;

  const percentage = (projectsCount / subscription.plano.max_projetos) * 100;
  const isNearLimit = percentage > 80;

  return (
    <div className={`p-4 rounded ${isNearLimit ? 'bg-yellow-100' : 'bg-green-100'}`}>
      <div className="flex justify-between items-center mb-2">
        <span className="font-semibold">Plano {subscription.plano.nome}</span>
        <span className="text-sm">{subscription.dias_restantes} dias restantes</span>
      </div>
      
      <div className="mb-2">
        <div className="flex justify-between text-sm">
          <span>Projetos</span>
          <span>{projectsCount} / {subscription.plano.max_projetos}</span>
        </div>
        <div className="w-full bg-gray-200 rounded h-2">
          <div 
            className={`h-2 rounded ${isNearLimit ? 'bg-yellow-500' : 'bg-green-500'}`}
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>
      
      {isNearLimit && (
        <p className="text-sm text-yellow-700">
          ⚠️ Você está próximo do limite. <a href="/upgrade" className="underline">Fazer upgrade</a>
        </p>
      )}
    </div>
  );
};
```

### 8.3 Modal de Upgrade

```tsx
// UpgradeModal.tsx
import React from 'react';

interface UpgradeModalProps {
  currentPlanName: string;
  assinaturaId: number;
  onClose: () => void;
}

export const UpgradeModal: React.FC<UpgradeModalProps> = ({ 
  currentPlanName, 
  assinaturaId, 
  onClose 
}) => {
  const handleUpgrade = async (newPlanId: number) => {
    const response = await fetch(`/api/assinaturas/${assinaturaId}/alterar-plano`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ novo_plano_id: newPlanId })
    });

    if (response.ok) {
      alert('Plano alterado com sucesso!');
      window.location.reload();
    } else {
      const error = await response.json();
      alert(`Erro: ${error.error}`);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded-lg p-8 max-w-2xl">
        <h2 className="text-2xl font-bold mb-4">Fazer Upgrade</h2>
        <p className="mb-6">Plano atual: <strong>{currentPlanName}</strong></p>
        
        <div className="space-y-4">
          <div className="border rounded p-4 hover:border-blue-500 cursor-pointer"
               onClick={() => handleUpgrade(3)}>
            <h3 className="font-bold">PROFISSIONAL - R$ 299/mês</h3>
            <p>50 projetos • 200 lotes • Exportar SHP/DXF</p>
          </div>
          
          <div className="border rounded p-4 hover:border-blue-500 cursor-pointer"
               onClick={() => handleUpgrade(4)}>
            <h3 className="font-bold">ENTERPRISE - R$ 999/mês</h3>
            <p>Ilimitado • API Access • Suporte Dedicado</p>
          </div>
        </div>
        
        <button 
          onClick={onClose}
          className="mt-6 px-4 py-2 border rounded hover:bg-gray-100"
        >
          Cancelar
        </button>
      </div>
    </div>
  );
};
```

---

## 9. Fluxo Completo de Implementação

### Passo 1: Aplicar Migration no Banco

```bash
# Conectar ao banco de dados
psql -d ativoreal_geo -U seu_usuario

# Executar migration
\i /path/to/03_pay_as_you_go_schema.sql
```

### Passo 2: Testar APIs via Postman/Insomnia

1. **Listar Planos**: `GET /api/planos`
2. **Criar Assinatura Free**: `POST /api/assinaturas` com plano_id=1
3. **Consultar Assinatura**: `GET /api/assinaturas/current?usuario_id=123`
4. **Fazer Upgrade**: `POST /api/assinaturas/1/alterar-plano` com novo_plano_id=2

### Passo 3: Integrar com Frontend

1. Adicionar componente `PricingPlans` na landing page
2. Adicionar `UsageBadge` no dashboard do topógrafo
3. Implementar middleware para validar limites antes de criar projetos

### Passo 4: Integrar com Gateway de Pagamento

Ver `MODELO_PAY_AS_YOU_GO.md` seção "Integração com Gateway"

---

## 10. Troubleshooting

### Erro: "Usuário já possui assinatura ativa"

**Solução:** Cancele a assinatura anterior antes de criar uma nova:

```bash
curl -X POST https://sua-api.azurewebsites.net/api/assinaturas/1/cancelar
```

### Erro: "Limite de projetos atingido"

**Solução:** Faça upgrade do plano:

```bash
curl -X POST https://sua-api.azurewebsites.net/api/assinaturas/1/alterar-plano \
  -H "Content-Type: application/json" \
  -d '{"novo_plano_id": 3}'
```

### Query SQL para Verificar Assinaturas

```sql
-- Ver todas as assinaturas ativas
SELECT 
    a.id,
    a.usuario_id,
    p.nome as plano,
    p.preco_mensal,
    a.status,
    a.expira_em,
    EXTRACT(DAY FROM (a.expira_em - CURRENT_TIMESTAMP)) as dias_restantes
FROM assinaturas a
JOIN planos_pagamento p ON a.plano_id = p.id
WHERE a.status IN ('ATIVA', 'TRIAL')
ORDER BY a.criado_em DESC;
```

---

## 📞 Suporte

- **Documentação Completa**: Ver `MODELO_PAY_AS_YOU_GO.md`
- **Schema SQL**: Ver `database/init/03_pay_as_you_go_schema.sql`
- **Issues**: Abrir no GitHub

---

**Última atualização:** 31/01/2026  
**Versão:** 1.0
