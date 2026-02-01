# 📊 AGENT 1 CONSTRAINT BREAKDOWN

**Propósito**: Responder "O que limita a criação e ação dos agentes?"

---

## 🔍 20 Restrições Mapeadas

### **CATEGORIA: ABSOLUTO (❌ Sem flexibilidade)**

#### ✅ 1. NO LOCALHOST EVER
- **Limita**: Todas sugestões de teste local
- **Por quê**: Production-first. Azure cloud from day 1
- **Exemplos bloqueados**: `localhost:3000`, `swa start`, `func start`
- **Escape**: Nenhum (absolutamente proibido)

#### ✅ 2. NO MOCKS EVER  
- **Limita**: Geração de dados fake, APIs mock, "modo desenvolvimento"
- **Por quê**: Real Azure services expõem constraints reais (auth, scaling)
- **Exemplos bloqueados**: `mock_payment_gateway()`, `fake_postgis()`, test fixtures com fake data
- **Escape**: Nenhum (absolutamente proibido)

#### ✅ 3. PostgreSQL + PostGIS, SEM ORM auto-create
- **Limita**: Agent 1 não pode usar `metadata.create_all()`
- **Por quê**: Schema é verdade em SQL scripts, não em ORM
- **Exemplos bloqueados**: `Base.metadata.create_all(engine)`
- **Escape**: Nenhum (Agent 1 deve gerar `.sql` files only)

#### ✅ 4. SRID 4674 Obrigatório
- **Limita**: Todas geometrias devem usar SIRGAS 2000 (Brasil INCRA compliance)
- **Por quê**: Outra SRID quebra integridade do dado
- **Exemplos bloqueados**: `GEOMETRY(Polygon, 4326)`, `ST_Transform(geom, 3857)`
- **Escape**: Nenhum

#### ✅ 5. ST_IsValid Constraint em tudo
- **Limita**: Geometrias auto-intersecting, não-fechadas
- **Por quê**: PostGIS opera só em geometrias válidas
- **Exemplos bloqueados**: Polygons self-intersecting, abertos
- **Escape**: Nenhum

#### ✅ 6. InfinitePay ONLY (MVP)
- **Limita**: Nenhum outro payment gateway
- **Por quê**: MVP scope = InfinitePay, Stripe/PayPal later
- **Exemplos bloqueados**: Stripe integration, Mercado Pago
- **Escape**: Nenhum (até phase 2)

#### ✅ 7. Multiple Clients per Project (Design Requirement)
- **Limita**: Schema DEVE suportar 1 projeto → N clientes
- **Por quê**: Caso normal (DESMEMBRAMENTO, LOTEAMENTO tem múltiplos clientes)
- **Exemplos bloqueados**: Foreign key `project_id UNIQUE`, 1:1 relação
- **Escape**: Nenhum (arquitetura fundamental)

#### ✅ 8. No Mocks em Schema
- **Limita**: Extra tables devem ser real, não test/dummy
- **Por quê**: Fixtures diferem de schema
- **Exemplos bloqueados**: Tabela `test_data`, `mock_surveys`, `temporary_stuff`
- **Escape**: Nenhum

### **CATEGORIA: HARD (✅ Exception com justificativa forte)**

#### 🔓 9. Azure Native Obrigatório
- **Limita**: Deve usar Azure services (não AWS, não self-hosted)
- **Por quê**: Cloud-first SaaS na Azure
- **Pode violar se**: Improvement arquitetônico substantial + documentado
- **Exemplos permitidos com justificativa**: "Usar DuckDB em vez de PostGIS porque X, Y, Z"

#### 🔓 10. Azure Functions Backend (Não Flask/Django/FastAPI)
- **Limita**: Backend em Python, mas rodar em Azure Functions (não servidor próprio)
- **Por quê**: Serverless cost model (pay-per-use vs. always-on VMs)
- **Pode violar se**: "FastAPI com ASGI adapter custa 60% menos + 3 features boas"
- **Requisito**: Trade-off documentation + approval

#### 🔓 11. No Direct Gov API Integration (MVP)
- **Limita**: SIGEF/CAR/FUNAI como URLs WMS manual, não direct API calls
- **Por quê**: Gov APIs unreliable, frequent changes. WMS = stable fallback
- **Pode violar se**: "Temos contrato SIGEF + API stable agora"
- **Fallback**: Se API falha, ativa WMS URL manual - NUNCA bloqueia o app

### **CATEGORIA: MEDIUM (⚠️ Customizável, case-by-case)**

#### 🔧 12. JWT 30min Expiry (Default)
- **Limita**: Tokens expiram em 30 min por padrão
- **Por quê**: Balance entre segurança (XSS) e UX (re-auth frequency)
- **Pode customizar**: Sim, se use case justifica (ex: internal dashboard = 2h ok)
- **Padrão**: 30 min para todos (clients + topógrafos)

#### 🔧 13. Role-Based Project Visibility (Strict)
- **Limita**: Topógrafo vê APENAS projetos que criou (não todos do sistema)
- **Por quê**: Privacy + performance (querys filtram por user_id)
- **Pode customizar**: Não (é strict rule, enforced in code)
- **Arquitetura**: Todos endpoints têm `WHERE user_id = :user_id`

#### 🔧 14. WMS Manual URLs Only
- **Limita**: Topógrafo input URLs manualmente (sem auto-pulling gov data)
- **Por quê**: Controle + simplicity. Gov data pulled só se topógrafo quer
- **Pode customizar**: Sim, pode adicionar auto-fetch layer depois (phase 2)

#### 🔧 15. Modular React Components (15+ Normal)
- **Limita**: Não há limite de componentes (15+ é NORMAL, não crime)
- **Por quê**: Modularidade = testability + reuse
- **Guideline**: Split by responsibility (map ≠ form ≠ sidebar)
- **Anti-pattern**: Mega-component com 1000+ linhas

#### 🔧 16. Agent 1 Extra Tables (até 200 allowed)
- **Limita**: Core = 6 tabelas (users, projects, lots, wms_layers, payments, chat_messages)
- **Permite**: Adicionar extras (audit_logs, notifications, etc.) até 200
- **Restrição**: Real entities only, não mock/test, não interfere core
- **Customiza**: Sim, por caso

### **CATEGORIA: STATUS INFO (ℹ️ Informação, sem bloqueio)**

#### ℹ️ 17. Node/Python Pré-instalado (Não agent-installable)
- **Status**: Provisionado via Azure runtime stack/build config
- **Por quê**: Agent não pode fazer `apt-get install` ou `brew install`
- **Implicação**: Node/Python vêm do **Runtime Stack** (Azure Functions) e do **node-version** no build da SWA
- **Bloqueador**: Não (responsabilidade de infra/configuração)

#### ℹ️ 18. Azure Database PostgreSQL NÃO configurado por Agent 1
- **Status**: Agent 1 gera `.sql` files, NOT deploy
- **Por quê**: Infrastructure = ops/DevOps job
- **Implicação**: Agent 1 precisa DATABASE_URL para testar, mas não set up
- **Bloqueador**: Sim para validação, não para geração de scripts

#### ℹ️ 19. OPENROUTER_API_KEY (Opcional, já setada)
- **Status**: Já uploaded em VS Code session
- **Por quê**: Internal dev tool (Jamba), não product feature
- **Implicação**: Agent pode usar se precisa code generation help
- **Bloqueador**: Não (se perder, retrieve backup)

#### ℹ️ 20. INFINITEPAY_API_KEY (Stand-by, não bloqueador agora)
- **Status**: Precisa só para Agent 4 (Payments)
- **Por quê**: MVP Agents 1-3 não precisam payment testing
- **Implicação**: Agent 1-3 podem rodar sem ela
- **Bloqueador**: Não para 1-3, Sim para 4 (deixa para depois)

---

## 🎯 Impacto por Agent

### **Agent 1: Engenheiro de Dados**
**Restrições que AFETAM diretamente**: #1, #2, #3, #4, #5, #7, #8, #16, #17, #18
**Restrições que AFETAM indiretamente**: #6 (design para payments), #10 (JSON responses)
**Resolvidas com**: DATABASE_URL + Agent 1 pode rodar completo

### **Agent 2: Backend Python**
**Restrições que AFETAM diretamente**: #1, #2, #6, #10, #12, #13, #15, #18
**Bloqueadores**: JWT_SECRET (para auth_middleware)
**Decisões de design**: 
- Usar Azure Functions (obrigatório) vs. Flask (discutível)
- JWT 30min default (respeitado) vs. customização (justificada)

### **Agent 3: Frontend React**
**Restrições que AFETAM**: #1, #2, #13 (role visibility), #14 (WMS URLs), #15 (components)
**Nenhum bloqueador**: React development é independent
**Decisões de design**: Component count (15+ ok), UI libraries (MUI/Ant Design ok)

### **Agent 4: Payments**
**Restrições que AFETAM diretamente**: #1, #2, #6, #12, #13
**Bloqueador absoluto**: INFINITEPAY_API_KEY
**Pré-requisito**: Agent 2 deployed (need endpoint URL)

---

## 🚨 Bloqueadores por Severidade

| Severidade | Componente | Bloqueador | Resolução | ETA |
|-----------|-----------|-----------|-----------|-----|
| 🔴 **CRÍTICO** | Agent 1 | DATABASE_URL não setado | Criar DB + set connection string | 5 min |
| 🔴 **CRÍTICO** | Agent 2 | JWT_SECRET não gerado | `python -c "import secrets; print(secrets.token_hex(32))"` | 2 min |
| 🟡 **IMPORTANTE** | Agent 4 | INFINITEPAY_API_KEY não obtido | Request da provider ou test key | 24h+ |
| ⚪ **INFORMAÇÃO** | Todos | OPENROUTER_API_KEY backup | Já tá setada, retrieve se perder | N/A |

---

## 💡 "Por quê?" Explicações Resumidas

**NO LOCALHOST**: 
- Cloud deployment é constraint real. Testar local esconde bugs de auth, scaling, env vars.

**NO MOCKS**: 
- Real services (Azure Blob, Cosmos) têm latency, throttling, quotas que mocks escondem.

**PostgreSQL + PostGIS**: 
- Land data = spatial. PostGIS = industry standard. SQLAlchemy auto-schema = inflexível.

**SRID 4674**: 
- Brasil's official CRS (SIRGAS 2000). Outra SRID = incompatível com INCRA + gov data.

**ST_IsValid**: 
- PostGIS ops (ST_Intersects, ST_Within) falham silenciosamente em geom inválidas.

**InfinitePay only**: 
- MVP scope lock. Phase 2 = Stripe/Mercado Pago.

**Multiple clients/project**: 
- DESMEMBRAMENTO (splitting land) = multiple owners. LOTEAMENTO (subdividing land) = lots per client.

**Azure Functions**: 
- Serverless = pay-per-use. Flask/Django = always-on VM (10-50x mais caro).

**No direct gov API (MVP)**: 
- SIGEF/CAR APIs change frequently, unreliable. WMS URLs = topographer picks source.

---

## 🎓 Learning Path for Agents

**Before running Agent 1**:
1. Read: `.github/copilot-instructions.md` (architecture)
2. Read: `.agents/CONSTRAINTS.md` (this file - what's forbidden)
3. Understand: Why SRID 4674, ST_IsValid, multiple clients matter

**Before running Agent 2**:
1. Review Agent 1 output (schema structure)
2. Understand: JWT flow (30min expiry, roles)
3. Plan: How to validate geometries in Python (Shapely + GeoAlchemy2)

**Before running Agent 3**:
1. Review Agent 2 endpoints (what data available?)
2. Understand: OpenLayers Draw/Modify/Snap interactions
3. Plan: Component architecture (map, form, sidebar, controls, chat)

**Before running Agent 4**:
1. Review Agent 2 & 3 (where payment button lives?)
2. Understand: InfinitePay webhook flow
3. Plan: Payment status transitions in database

