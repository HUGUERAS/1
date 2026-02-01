# 🤖 ATIVO REAL: Agent System Index

## Quick Navigation

### 🎯 Main Documents
- **[Execution Summary](./EXECUTION_SUMMARY.md)** - Overall progress, all 4 agents status
- **[Constraints Reference](./CONSTRAINTS.md)** - 20 absolute/hard rules
- **[Environment Setup](./ENVIRONMENT_SETUP.md)** - Cloud configuration

### 🔧 Agent Instructions
1. **[Agent 1: Database Engineer](./agent-1-data-engineer/AGENT_INSTRUCTIONS.md)**
   - Mission: PostgreSQL schema + 7 tables
   - Status: ✅ **COMPLETE**
   - Validator: `validate_schema.py` (7 tables, 3 users, 2 projects, 2 lots)

2. **[Agent 2: Backend Engineer](./agent-2-backend-engineer/AGENT_INSTRUCTIONS.md)**
   - Mission: Azure Functions + 50+ endpoints
   - Status: 📝 Ready for verification
   - Key: `function_app.py`, `auth_middleware.py`, `models.py`

3. **[Agent 3: Frontend Engineer](./agent-3-frontend-engineer/AGENT_INSTRUCTIONS.md)**
   - Mission: React/Vite SPA + OpenLayers map
   - Status: 📝 Design complete
   - Key: `GlobalMap.tsx`, `ClientPortal.tsx`, `TopographerDashboard.tsx`

4. **[Agent 4: Payments Engineer](./agent-4-payments-engineer/AGENT_INSTRUCTIONS.md)**
   - Mission: InfinitePay webhook + payment flow
   - Status: 📝 Design complete
   - Key: `POST /api/payments/webhook/infinitepay`

---

## 📊 Current Architecture

```
┌─────────────────────────────────────────────┐
│  Azure Static Web App (Frontend)            │
│  ├── React/Vite SPA                         │
│  ├── OpenLayers map + WMS layers            │
│  └── Client portal + Topographer dashboard  │
└────────────────┬────────────────────────────┘
                 │ API calls to /api/*
┌────────────────▼────────────────────────────┐
│  Azure Functions (Backend - Agent 2)        │
│  ├── Auth endpoints (JWT + roles)           │
│  ├── Project/Lot CRUD                       │
│  ├── Payment webhook handler                │
│  └── Chat messaging                         │
└────────────────┬────────────────────────────┘
                 │ SQLAlchemy ORM
┌────────────────▼────────────────────────────┐
│  Azure PostgreSQL (Agent 1 Schema)          │
│  ├── 7 tables (users, projects, lots, etc)  │
│  ├── 5 enums (roles, statuses)              │
│  └── JSONB geometry (no PostGIS)            │
└─────────────────────────────────────────────┘
```

---

## 🚀 Agent Execution Status

### Phase 1: Database (Agent 1)
✅ **COMPLETE** - 31/01/2026 10:45 UTC
- Schema created + deployed to `ativo-real-db.postgres.database.azure.com`
- 7 tables: users (3), projects (2), lots (2), wms_layers (2), payments, chat_messages, audit_log
- 5 enums configured
- Test data inserted
- Validator script passes all checks

**Files Created**:
- `agent-1-data-engineer/01_schema_clean.sql` (200 lines)
- `agent-1-data-engineer/execute_schema.py` (90 lines)
- `agent-1-data-engineer/validate_schema.py` (75 lines)

### Phase 2: Backend (Agent 2)
📝 **READY FOR REVIEW** - Instructions created 31/01/2026
- 50+ endpoints in `novo-projeto/backend/function_app.py`
- JWT auth, role-based access control (TOPOGRAFO|CLIENTE)
- Pydantic validation, SQLAlchemy ORM
- Spatial validation in `logic_services.py`

**Next Steps**:
- Verify all endpoints work with Agent 1 schema
- Test authentication flow
- Add comprehensive error handling
- Deploy to Azure Functions

### Phase 3: Frontend (Agent 3)
📝 **READY FOR BUILD** - Instructions created 31/01/2026
- React/Vite SPA with OpenLayers map
- Client portal (magic link access)
- Topographer dashboard (project management)
- WMS layer visualization
- File import/export (KML, GeoJSON, PDF)
- Payment integration redirect

**Next Steps**:
- Build React components (GlobalMap, ClientPortal, Dashboard)
- Implement typed API client
- Test magic link flow
- Deploy to Static Web App

### Phase 4: Payments (Agent 4)
📝 **READY FOR BUILD** - Instructions created 31/01/2026
- InfinitePay payment request creation
- Webhook handler with HMAC signature verification
- Payment status tracking
- Idempotency checks for duplicate webhooks
- Audit logging

**Next Steps**:
- Implement payment endpoint
- Build webhook handler
- Test payment flow (PIX, Boleto, Card)
- Add error handling

---

## 🎯 Key Files Reference

### Agent 1 (Database)
```
.agents/
└── agent-1-data-engineer/
    ├── AGENT_INSTRUCTIONS.md
    ├── 01_schema_clean.sql       ← Main schema
    ├── execute_schema.py         ← Deployment script
    ├── validate_schema.py        ← Validator script
    └── reports/
        └── AGENT_1_COMPLETE.md
```

### Agent 2 (Backend)
```
novo-projeto/backend/
├── function_app.py               ← 50+ endpoints
├── auth_middleware.py            ← JWT tokens
├── models.py                     ← SQLAlchemy ORM
├── schemas.py                    ← Pydantic validation
├── logic_services.py             ← Business logic
└── database.py                   ← Session management

.agents/
└── agent-2-backend-engineer/
    └── AGENT_INSTRUCTIONS.md
```

### Agent 3 (Frontend)
```
novo-projeto/ativo-real/
├── src/
│   ├── components/
│   │   ├── GlobalMap.tsx
│   │   ├── ClientPortal.tsx
│   │   ├── TopographerDashboard.tsx
│   │   └── WmsLayerManager.tsx
│   ├── services/
│   │   └── api.ts                ← Typed API client
│   └── pages/
├── package.json
├── vite.config.ts
└── tailwind.config.js

.agents/
└── agent-3-frontend-engineer/
    └── AGENT_INSTRUCTIONS.md
```

### Agent 4 (Payments)
```
novo-projeto/backend/
└── function_app.py
    └── @app.route("/api/payments/*")

.agents/
└── agent-4-payments-engineer/
    └── AGENT_INSTRUCTIONS.md
```

---

## 🔗 Azure Resources

| Service | Name | Status | Connection |
|---------|------|--------|------------|
| Resource Group | `rg-ativo-real` | ✅ Ready | West Europe |
| PostgreSQL | `ativo-real-db` | ✅ Ready | `ativo-real-db.postgres.database.azure.com:5432` |
| Storage | `storativorealbkp` | ✅ Ready | Standard_LRS |
| Static Web App | `swa-ativo-real` | ✅ Ready | `green-mud-007f89403.1.azurestaticapps.net` |

**Credentials** (stored in Azure Key Vault):
- `DATABASE_URL` ✅ Set in SWA app settings
- `JWT_SECRET` ✅ Set in SWA app settings
- `INFINITEPAY_API_KEY` - To be added
- `INFINITEPAY_WEBHOOK_SECRET` - To be added

---

## 📋 Checklist: Next Immediate Actions

### For Agent 2 (Backend)
```
[ ] Review all 50+ endpoints in function_app.py
[ ] Verify endpoints work with Agent 1 schema (users, projects, lots)
[ ] Test JWT token flow (create, refresh, verify)
[ ] Add error handling for database exceptions
[ ] Add Azure Application Insights logging
[ ] Test all CRUD operations (projects, lots, payments)
[ ] Deploy to Azure Functions
[ ] Verify /api/* routes work from Static Web App
```

### For Agent 3 (Frontend)
```
[ ] Create React component structure
[ ] Implement GlobalMap.tsx (OpenLayers + Draw/Modify/Snap)
[ ] Build ClientPortal.tsx (form + map + payment + chat)
[ ] Build TopographerDashboard.tsx (project list + create)
[ ] Implement typed API client (api.ts)
[ ] Test magic link access ({token})
[ ] Build payment redirect to InfinitePay
[ ] Add file export (KML, GeoJSON, PDF)
[ ] Test end-to-end workflow
[ ] Build & deploy to Static Web App
```

### For Agent 4 (Payments)
```
[ ] Implement POST /api/payments/create
[ ] Implement POST /api/payments/webhook/infinitepay
[ ] Add HMAC signature verification
[ ] Add idempotency checks (duplicate webhook detection)
[ ] Test payment flow (PIX, Boleto, Card)
[ ] Add error handling + logging
[ ] Test webhook retry scenarios
[ ] Deploy webhook endpoint
```

---

## 📞 Useful Commands

```bash
# Database
python .agents/agent-1-data-engineer/validate_schema.py

# Backend
cd novo-projeto/backend
func start                          # Local testing only (NEVER for production)
func azure functionapp publish <app-name>

# Frontend
cd novo-projeto/ativo-real
npm run build
# Push to GitHub → auto-deploy to Static Web App

# Verify deployment
curl https://swa-ativo-real.azurestaticapps.net/api/health
```

---

## 🎓 Learning Resources

- **Copilot Instructions**: [copilot-instructions.md](../../.github/copilot-instructions.md)
- **Constraints Breakdown**: [CONSTRAINTS.md](./CONSTRAINTS.md)
- **Business Flow Diagram**: [FLUXO_MVP_REAL.md](../../novo-projeto/FLUXO_MVP_REAL.md)

---

**Last Updated**: 31/01/2026 10:50 UTC  
**Next Review**: After Agent 2 backend tests pass
