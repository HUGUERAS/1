# 📋 ATIVO REAL - CONSOLIDAÇÃO DE REQUISITOS

**Data:** 31/01/2026
**Status:** Esgotado após 17 versões e múltiplas tentativas
**Objetivo:** Documento único com TUDO que foi proposto

---

## 🎯 VISÃO GERAL

**Ativo Real** é uma **GeoPlatform para regularização fundiária**

**Problema que resolve:**
- Proprietários rurais precisam regularizar imóveis
- Processo exige validação de geometrias
- Sobreposição com terras indígenas, áreas protegidas
- Documentação complexa (SIGEF, FUNAI, ICMBio)

---

## 👥 PERFIS DE USUÁRIO

### 1. TOPÓGRAFO
**O que faz:**
- ✅ Cria projetos de regularização
- ✅ Desenha lotes no mapa (OpenLayers)
- ✅ Valida sobreposições com áreas governamentais
- ✅ Exporta relatórios técnicos
- ✅ Envia para proprietário revisar

**Ferramentas técnicas:**
- Desenho de polígonos (snap-to-grid)
- Cálculo de áreas em tempo real
- Validação topológica (ST_IsValid)
- Export GeoJSON/PDF/Excel

### 2. PROPRIETÁRIO
**O que faz:**
- ✅ Visualiza projeto criado por topógrafo
- ✅ Revisa desenho dos lotes
- ✅ Aprova ou rejeita
- ✅ Realiza pagamento do serviço
- ✅ Acesso ao relatório final

**Limitações:**
- Read-only no mapa
- Sem acesso a ferramentas técnicas
- Visualização simplificada

### 3. AGRICULTOR
**O que faz:**
- ✅ Gerencia CAR (Cadastro Ambiental Rural)
- ✅ Visualiza áreas produtivas
- ✅ Monitora conformidade ambiental
- ✅ Exporta dados para SFP

**Dados específicos:**
- Áreas de produção
- Áreas de preservação
- Mata ciliar
- Histórico de uso

---

## 🗺️ FUNCIONALIDADES POR MÓDULO

### 1. AUTENTICAÇÃO
**Status:** ❌ NÃO FUNCIONA (Login não aparece)
**Esperado:**
- ✅ Login com email/senha
- ✅ JWT tokens (access + refresh)
- ✅ Refresh token automático
- ✅ Logout
- ✅ Remember me (opcional)

**Endpoints necessários:**
```
POST /auth/login
POST /auth/refresh
POST /auth/logout
GET /auth/me
POST /auth/register
```

### 2. DASHBOARD TOPÓGRAFO
**Status:** ❌ NÃO FUNCIONA (carrega, mas vazio)
**Esperado:**

#### 2.1 KPIs Dashboard
```
┌─────────────────────────────────────┐
│ Projetos em Andamento: 5             │
│ Projetos Concluídos: 12              │
│ Área Total: 450.8 hectares           │
│ Financeiro: R$ 45.000 / R$ 28.000   │
└─────────────────────────────────────┘
```

#### 2.2 Tabela de Projetos
```
| Título | Local | Status | Área | Progresso | Ações |
|--------|-------|--------|------|-----------|-------|
| Proj A | SP | Em And | 45.8 | 65% | Editar/Visualizar |
| Proj B | MG | Concluído | 120.5 | 100% | Baixar |
```

#### 2.3 Botões de Ação
- 🆕 Criar novo projeto
- 📊 Gerar relatório
- 💾 Backup de dados
- ⚙️ Configurações

### 3. MAPA (OpenLayers)
**Status:** ❌ FALHAS (desenha mas não salva)
**Esperado:**

#### 3.1 Camadas Visíveis
```
☑ Meu Projeto (desenho atual)
☑ Áreas SIGEF
☑ Áreas FUNAI
☑ Áreas ICMBio
☑ Satélite (fundo)
☑ Rua (fundo alternativo)
```

#### 3.2 Ferramentas de Desenho
- ✏️ Desenhar polígono (com snap-to-grid)
- ✂️ Dividir lote
- 🗑️ Deletar seleção
- 🎯 Selecionar múltiplos
- 🔍 Zoom fit

#### 3.3 Validação em Tempo Real
```
Enquanto desenha:
- ✅ Polígono fechado?
- ✅ Válido topologicamente?
- ✅ Sem auto-intersecção?
- ⚠️ Sobrepõe FUNAI? (alerta)
- ⚠️ Sobrepõe Mata ciliar? (alerta)
```

#### 3.4 Salvar Geometrias
- ✅ Salva automaticamente ao desenhar
- ✅ Histórico de versões
- ✅ Undo/Redo
- ✅ Baixar GeoJSON

### 4. GESTÃO DE LOTES
**Status:** ❌ FALHAS (não cria layers)
**Esperado:**
```
Projeto "Gleba Rio Claro"
├── Lote 1: 45.8 ha (finalizado)
│   ├── Geometria validada ✅
│   ├── Sem sobreposição ✅
│   └── Relatório gerado ✅
├── Lote 2: 32.3 ha (em edição)
│   ├── Geometria pendente ⏳
│   └── Verificando sobreposições...
└── Lote 3: 18.5 ha (novo)
```

### 5. VALIDAÇÃO GEOMÉTRICA
**Status:** ❌ NÃO TESTADO
**Esperado:**

#### 5.1 Backend (PostGIS)
```sql
-- Validar geometria
SELECT ST_IsValid(geom) FROM lotes WHERE id = 1;

-- Calcular área
SELECT ST_Area(geom::geography) / 10000 as hectares FROM lotes;

-- Detectar sobreposição com FUNAI
SELECT COUNT(*) FROM lotes l
JOIN funai_areas f ON ST_Intersects(l.geom, f.geom)
WHERE l.id = 1;
```

#### 5.2 Frontend (Feedback)
```
✅ Geometria válida
📍 Área: 45.8 hectares
⚠️ Aviso: Sobrepõe 2.3 ha de FUNAI
❌ Erro: Polígono com auto-intersecção
```

### 6. DADOS GOVERNAMENTAIS
**Status:** ❌ API criada mas não testada
**Esperado:**

```
GET /api/governo/areas
Response:
[
  {
    "tipo": "SIGEF",
    "nome": "Fazenda Santa Maria",
    "coords": [[−47.89, −15.78], ...],
    "area_hectares": 450
  },
  {
    "tipo": "FUNAI",
    "nome": "Terra Indígena Santuário",
    "coords": [[−47.87, −15.80], ...],
    "area_hectares": 12000
  },
  {
    "tipo": "ICMBio",
    "nome": "Área de Preservação",
    "coords": [[−47.92, −15.76], ...],
    "area_hectares": 5000
  }
]
```

### 7. PAGAMENTOS (InfinitePay)
**Status:** ⏳ ISOLADO (comentado)
**Esperado:**
```
Plano 1: R$ 500 (Básico - até 3 lotes)
Plano 2: R$ 1.500 (Profissional - até 20 lotes)
Plano 3: R$ 5.000 (Enterprise - ilimitado)

Fluxo:
1. Proprietário seleciona plano
2. Redireciona para checkout InfinitePay
3. Pagamento confirmado
4. Ativa acesso
5. Email com recibo
```

### 8. RELATÓRIOS
**Status:** ❌ NÃO FUNCIONA
**Esperado:**

#### 8.1 Relatório PDF
```
RELATÓRIO DE REGULARIZAÇÃO FUNDIÁRIA
=====================================
Projeto: Gleba Rio Claro
Local: São Paulo - SP
Proprietário: José Souza
Data: 31/01/2026

RESUMO EXECUTIVO
- Área total: 450.8 ha
- Lotes: 3
- Status: 2 validados, 1 em análise

DESCRIÇÃO DOS LOTES
Lote 1 (45.8 ha)
├ Localização: UTM 23K 651234.5 7851234.5
├ Perímetro: 2.3 km
├ Status: ✅ Validado
├ Sobreposições: Nenhuma
└ Documento: [anexo GeoJSON]

[... mais lotes ...]

VALIDAÇÃO TÉCNICA
✅ Todas as geometrias válidas
✅ Sem auto-intersecções
✅ Perímetros fechados
⚠️ 2.3 ha em zona de proteção ambiental (FUNAI)
✅ Dentro de conformidade legal

ASSINATURA
_________________
Topógrafo: [nome]
Data: 31/01/2026
```

#### 8.2 Relatório Excel
```
lotes.xlsx
├── Sheet "Resumo"
│   └ Tabela com KPIs
├── Sheet "Geometrias"
│   └ Tabela com coords
└── Sheet "Validações"
    └ Status de cada lote
```

### 9. CHAT AI / ASSISTENTE
**Status:** ❌ CRIADO mas não integrado
**Esperado:**
```
Usuário: "Analise este projeto para sobreposições"
IA: "Analisando... Encontrei 2.3 ha de sobreposição com 
     Terra Indígena. Recomendo remover essa área ou 
     solicitar parecer especializado."

Usuário: "Gere um relatório em PDF"
IA: "Gerando relatório... Pronto! Baixe aqui: [link]"
```

### 10. GESTÃO DE USUÁRIOS & PERMISSÕES
**Status:** ❌ JWT existe mas sem RBAC
**Esperado:**
```
Topógrafo: criar, editar, validar, exportar
Proprietário: visualizar, comentar, pagar
Agricultor: visualizar CAR, exportar dados
Admin: ver tudo, gerenciar usuários
```

---

## 📊 ESTADO TÉCNICO ATUAL

### Backend (Python + Azure Functions)
```
✅ Estrutura básica (function_app.py)
✅ JWT autenticação
✅ Models SQLAlchemy definidos
✅ Database connection
✅ PostGIS inicializado
❌ Endpoints funcionais (login broken)
❌ Lógica de negócio
❌ Validações geométricas
❌ Integração com API governo
❌ Pagamentos (comentado)
```

### Frontend (React + OpenLayers)
```
✅ Estrutura React (App.tsx com rotas)
✅ OpenLayers importado
✅ Componentes criados (Dashboard, Map)
❌ Login não aparece
❌ Dashboard vazio
❌ Mapa com falhas no desenho
❌ Persistência de dados
❌ Validação em tempo real
❌ Camadas SIGEF/FUNAI não carregam
```

### Database (PostgreSQL + PostGIS)
```
✅ Conexão via SQLAlchemy
✅ PostGIS extensão carregada
❌ Schema não aplicado (01_schema.sql)
❌ Tabelas não criadas
❌ Dados de teste não inseridos
❌ Índices geoespaciais não configurados
```

---

## 🔥 O QUE REALMENTE PRECISA FUNCIONAR (MVP)

### Mínimo viável para HOJE:
1. ✅ Login (email/senha) → redirect para dashboard
2. ✅ Dashboard carrega lista de projetos do banco
3. ✅ Botão "Novo projeto" → abre modal
4. ✅ Mapa carrega com OpenLayers
5. ✅ Desenha polígono → salva em banco

### Isso equivale a:
- Backend: 3 endpoints (login, get projetos, post criar lote)
- Frontend: 2 páginas (login, dashboard)
- Database: 2 tabelas (users, projects)

### Tempo: 4-8 horas LIMPO

---

## 🆚 COMPARAÇÃO: ATUAL vs NECESSÁRIO

| O que prometemos | O que funciona | Prioridade |
|-----------------|----------------|-----------|
| Login | ❌ | CRÍTICA |
| Dashboard | ❌ | CRÍTICA |
| Mapa desenho | ⚠️ (com falhas) | CRÍTICA |
| Salvar geometrias | ❌ | CRÍTICA |
| Validação SIGEF | ❌ | ALTA |
| Chat AI | ⚠️ (não integrado) | BAIXA |
| Pagamentos | ❌ | MÉDIA |
| Relatórios | ❌ | MÉDIA |

---

## 💥 RECOMENDAÇÃO FINAL

**Atual:** Você tem 50% do código em estado "experimental-morto"

**Opções:**
1. **Continue arrumando** o que existe (vai levar semanas)
2. **Comece do zero** com MVP focado (5 dias de trabalho limpo)

**Minha recomendação:** 
Opção 2. Começar do zero MAS com este documento como "spec".

**Próximo passo:**
```
1. Backup do código atual (é estudo de caso)
2. Criar novo repo limpo
3. Implementar EXATAMENTE este MVP
4. Depois adicionar feature por feature
```

Concordo?
