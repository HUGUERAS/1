# 🤖 Agentes de IA para Bem Real SaaS

**Ambiente**: VS Code + OpenRouter (Jamba 1.7 para análise profunda)

Agentes especializados para estruturar e desenvolver o Bem Real SaaS de forma incremental.

---
@@
## 📚 Documentation Files
- **`.agents/CONSTRAINTS.md`** - Master reference of all constraints that limit agent creation/action (20 items mapped)
- **`.agents/ENVIRONMENT_SETUP.md`** - Setup checklist for DATABASE_URL, JWT_SECRET, API keys, and blocker resolution
- **`.github/copilot-instructions.md`** - Global AI coding agent guide (architecture, patterns, absolute rules)
- **`.agents/agent-1-data-engineer/AGENT_INSTRUCTIONS.md`** - Detailed mission for Agent 1 (database schema)
@@- **`.agents/CONSTRAINT_BREAKDOWN.md`** - 20 constraints mapped with impact analysis per agent (why they exist, when can violate)

## 📋 Roadmap de Agentes

| # | Nome | Responsabilidade | Status | Próximas |
|---|------|-----------------|--------|----------|
| 1 | **Engenheiro Dados** | PostgreSQL + PostGIS schema | 🚀 PRONTO | Fixtures + validação |
| 2 | **Backend Python** | Azure Functions (validação geométrica) | ⏳ Próximo | Endpoints REST |
| 3 | **Frontend React** | Interface cliente + topógrafo | ⏳ Fila | Single-page portal |
| 4 | **Integração Payment** | InfinitePay webhook + workflow | ⏳ Fila | Testes e2e |

---

## 🚀 Como Usar Agente 1

### Pré-requisitos
```bash
# 1. Verificar OPENROUTER_API_KEY
echo $OPENROUTER_API_KEY

# 2. Estar na raiz do projeto
cd c:\Users\User\cooking-agent\ai1
```

### Executar
```bash
# Ver instruções completas
cat .agents/agent-1-data-engineer/AGENT_INSTRUCTIONS.md

# Executar via Python
python .agents/agent-1-data-engineer/run.py schema
python .agents/agent-1-data-engineer/run.py fixtures
python .agents/agent-1-data-engineer/run.py validate

# Ou rodar tudo
python .agents/agent-1-data-engineer/run.py all
```

### Com VS Code + AI Assistant
1. Abra `.agents/agent-1-data-engineer/AGENT_INSTRUCTIONS.md`
2. Selecione o conteúdo
3. Envie para Copilot Chat ou Jamba via OpenRouter
4. IA vai gerar scripts SQL prontos para usar

---

## 📂 Estrutura de Agentes

```
.agents/
├── README.md (você está aqui)
├── agent-1-data-engineer/
│   ├── AGENT_INSTRUCTIONS.md    # O que o agente deve fazer
│   ├── run.py                    # Executor/orquestrador
│   ├── queries.sql               # Validação pós-implementação
│   └── schema-draft.sql (NOVO)  # Será gerado
├── agent-2-backend/              # Próximo agente
└── agent-3-frontend/             # Terceiro agente
```

---

## 🔄 Fluxo de Trabalho

1. **Ler AGENT_INSTRUCTIONS.md** → Entender escopo
2. **Copiar conteúdo** → Enviar para Jamba/Copilot
3. **Receber output SQL/código** → Revisar em VS Code
4. **Testar com queries.sql** → Validar integridade
5. **Commit para Git** → Rastrear progress

---

## 💡 Exemplo: Agente 1 em Ação

```
Você (prompt): 
"Agente, leia AGENT_INSTRUCTIONS.md e gere o schema SQL completo 
para novo-projeto/database/init/01_schema.sql"

Jamba (resposta):
✅ Gera CREATE TABLE, constraints, triggers, indexes
✅ Explica cada constraint de integridade geométrica
✅ Fornece queries de validação prontas

Você:
1. Copia o SQL
2. Roda em novo-projeto/database/init/01_schema.sql
3. Testa com queries.sql
4. Commit: "feat: db schema com PostGIS + integridade geométrica"
```

---

## 🎯 Metas por Agente

### ✅ Agente 1: Dados (Esta semana)
- [ ] Schema PostgreSQL completo (7 tabelas)
- [ ] Constraints geométricos rigorosos (ST_IsValid, ST_Within)
- [ ] Fixtures com 20+ registros realistas
- [ ] Queries de validação passando

### ⏳ Agente 2: Backend (Próxima semana)
- [ ] 12 endpoints Azure Functions
- [ ] Validação de geometria com Shapely
- [ ] PostGIS queries integradas
- [ ] Testes automatizados

### ⏳ Agente 3: Frontend (Duas semanas)
- [ ] Single-page client portal
- [ ] Topographer dashboard com múltiplos clientes
- [ ] OpenLayers map + Draw/Modify
- [ ] Integração com Backend

### ⏳ Agente 4: Payment (Três semanas)
- [ ] InfinitePay webhook
- [ ] Status de pagamento real-time
- [ ] Pipeline completo (cliente → pago → entregue)

---

## 🚨 Regras para Todos os Agentes

**NUNCA:**
- ❌ Sugerir localhost ou mock data
- ❌ Criar código sem testar em Azure
- ❌ Usar ORM auto-create ao invés de SQL scripts
- ❌ Ignorar constraints de integridade geométrica

**SEMPRE:**
- ✅ Cloud-first (Azure Functions + PostgreSQL)
- ✅ Real integrations (sem mocks)
- ✅ SRID 4674 para Brasil
- ✅ Múltiplos clientes por projeto (normal)

---

## 📞 Suporte

- **Copilot Instructions**: `.github/copilot-instructions.md`
- **Dev Tools**: `backend/jamba_openrouter.py`
- **Setup Guide**: `OPENROUTER_QUICKSTART.md`

---

**Pronto para começar com Agente 1? Execute:** 
```
python .agents/agent-1-data-engineer/run.py all
```

🚀 **Vamos construir Bem Real!**
