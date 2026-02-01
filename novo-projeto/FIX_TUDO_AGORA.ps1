#!/usr/bin/env pwsh
# ============================================
# SCRIPT DE CORREÇÃO COMPLETA - ATIVO REAL
# ============================================
# Execução: .\FIX_TUDO_AGORA.ps1
# ============================================

Write-Host "🚀 INICIANDO CORREÇÃO COMPLETA DO PROJETO" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"
$startLocation = Get-Location

try {
    # ============================================
    # ETAPA 1: LIMPEZA DE ESTRUTURA
    # ============================================
    Write-Host "📂 ETAPA 1/5: Reorganizando estrutura de pastas..." -ForegroundColor Yellow
    
    # 1.1 Criar pasta .archive se não existir
    if (-not (Test-Path ".archive")) {
        New-Item -ItemType Directory -Path ".archive" | Out-Null
        Write-Host "  ✅ Pasta .archive criada" -ForegroundColor Green
    }
    
    # 1.2 Mover documentação legada
    $docsLegados = @(
        "CHECKLIST_FINAL_DEPLOY.md",
        "CHECKPOINT_31_01_2026.md",
        "COMECE_AQUI_DEPLOY.md",
        "CONFIGURAR_POWERSHELL.md",
        "DEPLOY_AZURE_DIRETO.md",
        "DEPLOY_EXPRESS.md",
        "DEPLOY_GUIDE.md",
        "DEPLOY_INSTRUCTIONS.md",
        "EXECUTE_DEPLOY_AGORA.md",
        "FREE_AI_OPTIONS.md",
        "GUIA_PRATICO_PAY_AS_YOU_GO.md",
        "GUIA_TESTE_RAPIDO.md",
        "IMPLEMENTACAO_FINAL_COMPLETA.md",
        "INDICE_PAY_AS_YOU_GO.md",
        "INTEGRACAO_LOVABLE_PAY_AS_YOU_GO.md",
        "ISOLAMENTO_INFINITEPAY_31_01.md",
        "JAMBA_INTEGRATION.md",
        "MODELO_PAY_AS_YOU_GO.md",
        "MVP_PLANO_EXECUCAO.md",
        "OPENROUTER_INTEGRATION.md",
        "OPENROUTER_QUICKSTART.md",
        "PROPOSTA_ARQUITETURA_SINGLE_PAGE_LOGIN.md",
        "QUICK_START_OPENROUTER.md",
        "README_PAY_AS_YOU_GO.md",
        "REFACTORING_PLAN.md",
        "REQUIREMENTS_CONSOLIDADO.md",
        "RESUMO_EXECUTIVO_PAY_AS_YOU_GO.md",
        "SOLUCOES_IMPLEMENTADAS.md",
        "TESTES_AUTENTICACAO.md",
        "TESTE_OPENROUTER.md",
        "TESTE_OPENROUTER_RESULTADO.md",
        "FLUXO_MVP_REAL.md",
        "FLUXO_REAL_TOPOGRAFO_CLIENTE.md"
    )
    
    $movedCount = 0
    foreach ($doc in $docsLegados) {
        if (Test-Path $doc) {
            Move-Item -Path $doc -Destination ".archive\" -Force
            $movedCount++
        }
    }
    Write-Host "  ✅ $movedCount documentos arquivados" -ForegroundColor Green
    
    # 1.3 Renomear frontend para frontend-legacy
    if (Test-Path "frontend" -and -not (Test-Path "frontend-legacy")) {
        Rename-Item -Path "frontend" -NewName "frontend-legacy"
        Write-Host "  ✅ frontend/ renomeado para frontend-legacy/" -ForegroundColor Green
    }
    
    Write-Host ""
    
    # ============================================
    # ETAPA 2: ATUALIZAR README.md
    # ============================================
    Write-Host "📝 ETAPA 2/5: Atualizando README.md (removendo localhost)..." -ForegroundColor Yellow
    
    $readmeContent = @"
# Ativo Real - GeoPlatform 🌍

Plataforma de gestão fundiária e topografia com validação geométrica inteligente.

## 🏗️ Arquitetura (Azure Native)

Este projeto é Cloud-Native, utilizando o ecossistema Azure para performance e baixo custo.

*   **Frontend**: React + TypeScript + Ant Design + OpenLayers (Hospedado no **Azure Static Web Apps**)
*   **Backend**: Python Serverless (**Azure Functions v2**)
*   **Banco de Dados**: PostgreSQL com PostGIS (**Azure Database for PostgreSQL**)

### 🛡️ Diferenciais de Engenharia

1.  **Validação Geométrica no Backend**: O Frontend é apenas para desenho. A matemática pesada (interseções, sobreposições) é feita no Python usando ``Shapely`` e ``GeoAlchemy2`` antes de salvar no banco.
2.  **Topologia Rígida**: O banco de dados (PostGIS) possui constraints ``CHECK(ST_IsValid(geom))`` para impedir dados corrompidos.
3.  **Separação de Preocupações**:
    *   ``ativo-real/``: Frontend principal (React + TS)
    *   ``backend/logic_services.py``: Regras de negócio puras (testáveis)
    *   ``backend/function_app.py``: Camada de adaptação HTTP (Azure Functions)

## 📂 Estrutura do Projeto

````
novo-projeto/
├── ativo-real/               # Frontend Principal (React + TypeScript)
│   ├── src/
│   │   ├── components/       # Componentes UI
│   │   ├── pages/            # Páginas (dashboards)
│   │   ├── services/         # API clients
│   │   └── types/            # TypeScript types
│   └── staticwebapp.config.json
├── backend/                  # Azure Functions (Python)
│   ├── function_app.py       # Entrypoint da API
│   ├── logic_services.py     # Lógica de Negócios
│   ├── models.py             # Modelos de Banco (SQLAlchemy)
│   ├── openrouter_client.py  # Integração AI
│   └── requirements.txt
├── database/                 # Scripts SQL
│   └── init/
│       └── 01_schema.sql     # Schema PostGIS completo
├── frontend-legacy/          # ⚠️ IGNORAR (versão antiga)
├── .archive/                 # 📦 Documentação histórica
├── README.md                 # 📖 Este arquivo
├── ARCHITECTURE_SPECS.md     # 🏗️ Referência técnica detalhada
└── PROJECT_STATUS.md         # 📊 Status atual do projeto
````

## 🚀 Deploy no Azure

**⚠️ IMPORTANTE**: Este projeto NÃO usa localhost. Todo desenvolvimento é feito direto no Azure.

### Pré-requisitos
*   Conta Azure ativa
*   Azure CLI instalado (``az login``)
*   Git configurado

### 1. Criar Azure Static Web App

````bash
az login

az staticwebapp create \
  --name ativo-real-prod \
  --resource-group seu-resource-group \
  --source https://github.com/seu-usuario/seu-repo \
  --location "East US 2" \
  --branch main \
  --app-location "ativo-real" \
  --api-location "backend" \
  --output-location "dist"
````

### 2. Criar Banco de Dados PostgreSQL

````bash
az postgres flexible-server create \
  --name ativo-real-db \
  --resource-group seu-resource-group \
  --location "East US 2" \
  --admin-user dbadmin \
  --admin-password "SuaSenhaSegura123!" \
  --sku-name Standard_B1ms \
  --version 14 \
  --storage-size 32

# Rodar schema
psql -h ativo-real-db.postgres.database.azure.com \
     -U dbadmin \
     -d postgres \
     -f database/init/01_schema.sql
````

### 3. Configurar Variáveis de Ambiente

No Azure Portal > Static Web App > Configuration, adicione:

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| ``DATABASE_URL`` | PostgreSQL connection string | ✅ Sim |
| ``JWT_SECRET`` | Token signing key (gere com ``openssl rand -hex 32``) | ✅ Sim |
| ``OPENROUTER_API_KEY`` | AI features (análise topográfica) | ⚠️ Opcional |
| ``INFINITEPAY_API_KEY`` | Payment gateway | ⚠️ Opcional (stand-by) |

### 4. Deploy Automático

Cada push para ``main`` dispara deploy automático via GitHub Actions.

## 📊 Status do Projeto

Ver **PROJECT_STATUS.md** para detalhes completos.

**Resumo Rápido**:
- ✅ Backend completo (12+ endpoints, auth JWT, AI integration)
- ✅ Frontend principal (ativo-real/) com dashboards e mapas
- ✅ Database schema com PostGIS (SRID 4674 - SIRGAS 2000)
- ⏳ Integração frontend ↔ backend (em finalização)

## 🔐 Segurança

*   Autenticação JWT (30min access token, 7 dias refresh token)
*   Magic links para clientes (7 dias de validade)
*   Role-based access control (TOPOGRAFO, CLIENTE, ADMIN)
*   Geometria validada no backend (evita ataques de dados inválidos)

## 📚 Documentação Técnica

*   **ARCHITECTURE_SPECS.md** - Arquitetura detalhada, fluxos, constraints
*   **PROJECT_STATUS.md** - Status atual, próximos passos
*   **.agents/CONSTRAINTS.md** - Regras e limitações do projeto
*   **backend/README.md** - Documentação da API (endpoints, schemas)

## 🆘 Suporte

Para perguntas sobre o projeto, consulte:
1. **PROJECT_STATUS.md** (estado atual)
2. **ARCHITECTURE_SPECS.md** (decisões técnicas)
3. **.agents/CONSTRAINTS.md** (regras absolutas)

---

**Desenvolvido com Azure Functions + PostGIS + React TypeScript** 🚀
"@
    
    Set-Content -Path "README.md" -Value $readmeContent -Encoding UTF8
    Write-Host "  ✅ README.md atualizado (localhost removido)" -ForegroundColor Green
    Write-Host ""
    
    # ============================================
    # ETAPA 3: CRIAR PROJECT_STATUS.md
    # ============================================
    Write-Host "📊 ETAPA 3/5: Criando PROJECT_STATUS.md..." -ForegroundColor Yellow
    
    if (-not (Test-Path "PROJECT_STATUS.md")) {
        $statusContent = @"
# 📊 Project Status - Ativo Real

**Última atualização**: 01/02/2026

## ✅ O Que Está Pronto

### Backend (Azure Functions)
- ✅ Autenticação JWT completa (login, refresh, magic links)
- ✅ Endpoints CRUD (projetos, lotes, usuários)
- ✅ Integração OpenRouter (AI chat, análise topográfica)
- ✅ Validação geométrica (PostGIS + Shapely)
- ✅ WMS layers management
- ✅ Chat messages
- ✅ Status history
- ✅ Assinaturas (pay-as-you-go model)

### Frontend (ativo-real/)
- ✅ React + TypeScript + Ant Design
- ✅ OpenLayers map com Draw/Modify/Snap
- ✅ Dashboard topógrafo
- ✅ Portal do cliente (single-page)
- ✅ Formulários (urbano, rural)
- ✅ Chat widget
- ✅ Status timeline
- ✅ File upload/download
- ✅ Dark mode
- ✅ Ícones e logo customizados

### Database
- ✅ PostgreSQL + PostGIS schema (01_schema.sql)
- ✅ Constraints geométricos (ST_IsValid, ST_Within)
- ✅ SRID 4674 (SIRGAS 2000)
- ✅ Triggers de histórico de status

## 🚧 Em Desenvolvimento

- ⏳ InfinitePay webhook implementation (backend pronto, testes pendentes)
- ⏳ Integração completa frontend ↔ backend
- ⏳ Testes end-to-end

## 📂 Estrutura Oficial

````
novo-projeto/
├── ativo-real/              # ✅ FRONTEND OFICIAL (React + TS)
├── backend/                 # ✅ BACKEND OFICIAL (Azure Functions)
├── database/                # ✅ SQL SCRIPTS
├── frontend-legacy/         # ⚠️  LEGADO (ignorar)
├── .archive/                # 📦 Documentação histórica
├── README.md               # 📖 Guia principal
├── ARCHITECTURE_SPECS.md   # 🏗️  Referência técnica
└── PROJECT_STATUS.md       # 📊 Este arquivo
````

## 🎯 Próximos Passos

1. **Deploy Azure**: Configurar Static Web App + PostgreSQL
2. **Testes E2E**: Validar fluxo completo (topógrafo → cliente → pagamento)
3. **Documentação**: Atualizar ARCHITECTURE_SPECS.md com mudanças recentes

## 📝 Notas Importantes

- **FRONTEND PRINCIPAL**: Use ``ativo-real/`` (não ``frontend-legacy/``)
- **NO LOCALHOST**: Desenvolvimento direto no Azure
- **CONSTRAINTS**: Ver ``.agents/CONSTRAINTS.md`` para regras absolutas
"@
        
        Set-Content -Path "PROJECT_STATUS.md" -Value $statusContent -Encoding UTF8
        Write-Host "  ✅ PROJECT_STATUS.md criado" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  PROJECT_STATUS.md já existe (mantido)" -ForegroundColor Yellow
    }
    
    Write-Host ""
    
    # ============================================
    # ETAPA 4: CRIAR .copilot-context.md
    # ============================================
    Write-Host "🤖 ETAPA 4/5: Criando .copilot-context.md (guia para Copilot)..." -ForegroundColor Yellow
    
    $copilotContext = @"
# Contexto do Projeto - Ativo Real

**LEIA ISSO PRIMEIRO ANTES DE QUALQUER RESPOSTA**

## 🎯 Projeto

Plataforma SaaS de topografia/georreferenciamento para Brasil.
- Topógrafos criam projetos e lotes
- Clientes acessam via magic link
- Geometria validada com PostGIS (SRID 4674)

## 📂 Estrutura Oficial

| Pasta | Status | Descrição |
|-------|--------|-----------|
| ``ativo-real/`` | ✅ **USAR** | Frontend principal (React + TypeScript) |
| ``backend/`` | ✅ **USAR** | Azure Functions (Python) |
| ``database/`` | ✅ **USAR** | SQL scripts PostGIS |
| ``frontend-legacy/`` | ❌ **IGNORAR** | Versão antiga (não usar) |
| ``.archive/`` | 📦 **HISTÓRICO** | Docs antigos (referência) |

## 🚫 REGRAS ABSOLUTAS (NUNCA VIOLAR)

1. **NO LOCALHOST**: Projeto roda APENAS no Azure. Não sugerir ``localhost``, ``swa start``, ``func start``
2. **NO MOCKS**: Integrações reais (Azure Functions, PostgreSQL, InfinitePay)
3. **Frontend = ativo-real/**: Não mencionar ``frontend/`` ou ``frontend-legacy/``
4. **SRID 4674**: Geometrias sempre com SIRGAS 2000 (Brasil)
5. **PostgreSQL + PostGIS**: Não sugerir outros bancos

## ✅ Tecnologias Confirmadas

- **Frontend**: React 18 + TypeScript + Ant Design + OpenLayers
- **Backend**: Azure Functions v2 (Python 3.11)
- **Database**: PostgreSQL 14 + PostGIS 3.x
- **Auth**: JWT (30min access, 7d refresh)
- **AI**: OpenRouter (Jamba 1.7 - opcional)
- **Payments**: InfinitePay (PIX/Card/Boleto)

## 📄 Documentação Prioritária

Quando responder perguntas, consultar NESTA ORDEM:
1. ``PROJECT_STATUS.md`` (status atual)
2. ``ARCHITECTURE_SPECS.md`` (decisões técnicas)
3. ``backend/function_app.py`` (API real)
4. ``ativo-real/src/`` (código frontend real)

## 🔍 Como Responder Perguntas

**ANTES de responder**:
- ✅ Verificar se contexto é sobre ``ativo-real/`` (correto) ou ``frontend/`` (legado)
- ✅ Nunca sugerir localhost ou desenvolvimento local
- ✅ Referenciar Azure Functions, não Flask/FastAPI standalone
- ✅ Confirmar SRID 4674 em queries geométricas

**Perguntas Comuns**:
- "Como rodar o projeto?" → **Azure deploy, não localhost**
- "Onde está o frontend?" → **ativo-real/ (não frontend/)**
- "Como adicionar endpoint?" → **Editar backend/function_app.py (Azure Function decorator)**
- "Qual CRS usar?" → **SRID 4674 (SIRGAS 2000)**

## 📊 Estado Atual (02/02/2026)

- Backend: **90% completo** (12 endpoints, auth, AI)
- Frontend: **85% completo** (falta integração final)
- Database: **100% completo** (schema pronto)
- Deploy: **Pendente** (aguardando config Azure)

## 🎯 Próximos Passos

1. Integração frontend ↔ backend (connect API calls)
2. Deploy Azure (Static Web App + PostgreSQL)
3. Testes E2E

---

**Se tiver dúvida sobre o projeto, consulte PROJECT_STATUS.md primeiro!**
"@
    
    Set-Content -Path ".copilot-context.md" -Value $copilotContext -Encoding UTF8
    Write-Host "  ✅ .copilot-context.md criado (Copilot vai ler isso primeiro!)" -ForegroundColor Green
    Write-Host ""
    
    # ============================================
    # ETAPA 5: VALIDAÇÃO FINAL
    # ============================================
    Write-Host "✅ ETAPA 5/5: Validando estrutura final..." -ForegroundColor Yellow
    
    Write-Host ""
    Write-Host "📂 Estrutura de Pastas:" -ForegroundColor Cyan
    Get-ChildItem -Directory | Where-Object { $_.Name -notlike "__*" -and $_.Name -ne "node_modules" } | ForEach-Object {
        $emoji = switch ($_.Name) {
            "ativo-real" { "✅" }
            "backend" { "✅" }
            "database" { "✅" }
            ".archive" { "📦" }
            "frontend-legacy" { "⚠️ " }
            default { "📁" }
        }
        Write-Host "  $emoji $($_.Name)"
    }
    
    Write-Host ""
    Write-Host "📄 Documentos Principais:" -ForegroundColor Cyan
    Get-ChildItem -Filter "*.md" | Where-Object { $_.Name -notlike ".*" } | Select-Object -First 10 | ForEach-Object {
        Write-Host "  📝 $($_.Name)"
    }
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Green
    Write-Host "✅ CORREÇÃO COMPLETA FINALIZADA!" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🎯 PRÓXIMOS PASSOS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Comitar mudanças:" -ForegroundColor White
    Write-Host "   git add -A" -ForegroundColor Gray
    Write-Host "   git commit -m 'fix: alinha projeto com constraints Azure - remove localhost'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Deploy no Azure:" -ForegroundColor White
    Write-Host "   git push origin main" -ForegroundColor Gray
    Write-Host "   (GitHub Actions faz deploy automático)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Testar Copilot:" -ForegroundColor White
    Write-Host "   - Abra VS Code" -ForegroundColor Gray
    Write-Host "   - Pergunte: 'Qual é o frontend principal deste projeto?'" -ForegroundColor Gray
    Write-Host "   - Resposta esperada: 'ativo-real/' (não frontend/)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Consultar documentação:" -ForegroundColor White
    Write-Host "   - README.md → Deploy no Azure" -ForegroundColor Gray
    Write-Host "   - PROJECT_STATUS.md → O que está pronto" -ForegroundColor Gray
    Write-Host "   - .copilot-context.md → Guia para Copilot" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "📚 Arquivos criados/atualizados:" -ForegroundColor Cyan
    Write-Host "  ✅ README.md (localhost removido)" -ForegroundColor Green
    Write-Host "  ✅ PROJECT_STATUS.md (status completo)" -ForegroundColor Green
    Write-Host "  ✅ .copilot-context.md (guia Copilot)" -ForegroundColor Green
    Write-Host "  ✅ .archive/ ($movedCount docs arquivados)" -ForegroundColor Green
    Write-Host "  ✅ frontend-legacy/ (isolado)" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ ERRO: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Stack Trace:" -ForegroundColor Yellow
    Write-Host $_.Exception.StackTrace -ForegroundColor Gray
    exit 1
} finally {
    Set-Location $startLocation
}

Write-Host "🚀 Script concluído com sucesso!" -ForegroundColor Green
Write-Host ""
