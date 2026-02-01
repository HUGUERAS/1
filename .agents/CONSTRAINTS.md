# 🔒 Agent Constraints & Limitations Reference

**Updated**: 31/01/2026  
**Purpose**: Document all constraints that limit agent creation and action

---

## 📋 Master Constraint List

| # | Constraint | Type | Applies To | Flexibility | Notes |
|---|-----------|------|-----------|-------------|-------|
| 1 | **NO LOCALHOST** | Absolute | All agents | ❌ None | All development assumes Azure cloud deployment. NO `localhost:8000`, `swa start`, `func start`, or local testing. |
| 2 | **NO MOCKS** | Absolute | All agents | ❌ None | Real integrations with real Azure services only. No mock data, mock APIs, no "development mode". |
| 3 | **Azure Native Required** | Hard | All agents | ✅ Exception allowed | Must use Azure services (Functions, Static Web Apps, PostgreSQL, etc.). Can deviate if substantial improvement documented. |
| 4 | **PostgreSQL + PostGIS** | Hard | Database (Agent 1) | ❌ None | No ORM auto-create (`metadata.create_all()`). Schema defined by SQL scripts only. |
| 5 | **Azure Functions Only** | Medium | Backend (Agent 2) | ✅ Exception allowed | Primary: Azure Functions v2 (Python). Can use Flask/Django/FastAPI IF substantial architectural improvement justifies deviation (then document trade-offs). |
| 6 | **SRID 4674 Mandatory** | Hard | Database (Agent 1) | ❌ None | SIRGAS 2000 CRS mandatory for Brazil INCRA compliance. All geometries must use this SRID. |
| 7 | **ST_IsValid Constraint** | Hard | Database (Agent 1) | ❌ None | All geometries must pass `ST_IsValid()` check. No self-intersecting polygons, must be closed. |
| 8 | **No Gov API Direct Integration (MVP)** | Medium | Backend (Agent 2) | ✅ Phase 2+ | SIGEF/CAR/FUNAI: NO direct API calls in MVP. Use WMS layer URLs for visualization. Fallback: If API integration attempted and fails, apply WMS URLs manually - do NOT block functionality. Future phases may add direct API integration. |
| 9 | **WMS Manual URLs Only** | Medium | Frontend (Agent 3) | ⚠️ Documented | Topographer manually inputs WMS URLs (SIGEF, CAR, FUNAI endpoints). No automatic gov data pulling in MVP. |
| 10 | **InfinitePay Only** | Hard | Payments (Agent 4) | ❌ None | Single payment gateway: InfinitePay (PIX/Card/Boleto). No other providers in MVP. API key required but can be in stand-by if needed. |
| 11 | **Node/Python Must Exist** | Hard | Infrastructure | ❌ None | Cannot install Node.js or Python (assumed pre-installed in Azure environment). Agents work within existing runtime. |
| 12 | **JWT 30min Expiry (Default)** | Medium | Backend Auth | ✅ Customizable | Default session token expiry is 30 minutes. Can be customized for specific workflows if justified. Magic links (client access) are 7 days. |
| 13 | **Role-Based Project Visibility** | Medium | Backend Auth | ⚠️ Strict rule | Topographer sees ONLY projects they created (not all projects in system). Clients see only their assigned lot. |
| 14 | **Multiple Clients per Project** | Hard | Data Model (Agent 1) | ❌ None | NORMAL case, not exception. One project can have 1+ clients (property owners). Enforced by schema design (2 project types: INDIVIDUAL, DESMEMBRAMENTO, LOTEAMENTO). |
| 15 | **No ORM Auto-Creation** | Hard | Backend (Agent 2) | ❌ None | SQLAlchemy ORM exists but NO auto-schema creation. Schema is source of truth in SQL scripts. |
| 16 | **Modular React Components** | Medium | Frontend (Agent 3) | ✅ Flexible | 15+ components is NORMAL for complex UI. Expected: map, form, sidebar, controls, chat, etc. Split by responsibility; avoid monolithic mega-components. |
| 17 | **Agent 1 Table Flexibility** | Medium | Database (Agent 1) | ✅ Flexible | Core tables: 6 required. Can add extra tables (up to 200) if real, not mock, and don't interfere with core functionality. |
| 18 | **No Mocks in Schema** | Hard | Database (Agent 1) | ❌ None | Extra tables must be real business entities, not dummy data or test structures. |
| 19 | **Azure Database PostgreSQL Not Configured** | Status | Database (Agent 1) | ℹ️ Not Agent 1 job | Agent 1 creates SQL scripts; user/Agent 2+ handles Azure Database configuration and connection. |
| 20 | **OPENROUTER_API_KEY Stand-by** | Status | Dev Tools | ℹ️ Optional | If using Jamba/OpenRouter for code generation: API key optional, can be added later. Already uploaded in session. |

---

## 🎯 Constraint Categories

### **ABSOLUTE (Never Violate - ❌ No Flexibility)**
- NO LOCALHOST
- NO MOCKS
- PostgreSQL + PostGIS (no auto-create)
- SRID 4674 mandatory
- ST_IsValid constraint
- InfinitePay only (MVP)
- No Node/Python install
- Multiple clients per project (design must support it)
- No ORM auto-creation
- No mocks in schema

### **HARD (Violate Only for Major Improvement - ✅ Exception Possible)**
- Azure Native required
- Azure Functions primary backend
- No direct gov API integration (MVP phase)

### **MEDIUM (Customizable - ⚠️ Case-by-Case)**
- JWT 30min expiry (can customize)
- WMS manual URLs (documented approach)
- Role-based visibility (strict rule but enforced in code)
- Modular React components (15+ is normal, not limit)
- Agent 1 extra tables (up to 200 allowed)

### **STATUS (Informational - ℹ️ No Blocker)**
- Azure Database PostgreSQL config (not Agent 1 responsibility)
- OPENROUTER_API_KEY (optional, already uploaded)

---

## 💡 Why These Constraints Exist

**ABSOLUTE RULES Rationale**:
1. **NO LOCALHOST** → Production-first mentality. Cloud deployment is day-1 reality. No local testing rabbit holes.
2. **NO MOCKS** → Real Azure services enforce real constraints (auth, scaling, cost). Mock solutions hide integration bugs.
3. **PostgreSQL + PostGIS** → Land data is spatial; PostGIS is industry standard for Brazil INCRA compliance.
4. **SRID 4674** → Brazil's official geographic reference system. Other SRIDs create compliance + data exchange issues.
5. **ST_IsValid** → Invalid geometries break PostGIS operations (ST_Intersects, ST_Within, ST_Touches).

**HARD CONSTRAINTS Rationale**:
- **Azure Functions** → Serverless cost model matches topography SaaS (pay-per-use). Flask/Django require always-on VMs (higher cost).
- **No direct gov API (MVP)** → Gov APIs (SIGEF/CAR) are unreliable, frequently change. WMS URLs are stable fallback. Direct API integration is phase 2.

**MEDIUM CONSTRAINTS Rationale**:
- **JWT expiry** → 30min balances security (XSS risk) vs. UX (re-auth frequency). Customizable for high-trust scenarios (internal topographer dashboard).
- **WMS manual** → Gives topographer control without complexity. They understand their region's data sources.
- **React components** → 15+ is natural for complex UI (map = 1 component, form = 3-5 nested, sidebar = 2-3, controls = 3-5). Modularity improves testability + reuse.

**STATUS INFO Rationale**:
- **Azure Database config** → Agent 1 job: generate `.sql` scripts. Agent 2/Infra job: deploy to Azure (requires DATABASE_URL). Not Agent 1 blocker.
- **OPENROUTER_API_KEY** → Already uploaded. Optional for now. Needed only if using Jamba for code generation.

---

## 🔄 Constraint Application by Agent

### **Agent 1: Engenheiro de Dados (Database)**
- **Must respect**: Constraints #4, #6, #7, #14, #15, #17, #18
- **Should avoid**: #1, #2 (development happens in Azure)
- **Status**: #19 (configuration not Agent 1 job)

### **Agent 2: Backend Engineer (Azure Functions)**
- **Must respect**: Constraints #1, #2, #3, #5, #8, #10, #12, #13, #15
- **Hard stop**: Cannot use local dev, cannot mock InfinitePay, cannot hardcode secrets
- **Flexibility**: Can argue for alternative framework if strong architectural case (#5)

### **Agent 3: Frontend Engineer (React + OpenLayers)**
- **Must respect**: Constraints #1, #2, #9, #16
- **Design freedom**: Component count, UI libraries, styling approach - no limits
- **WMS note**: User provides URLs; Agent 3 displays them (#9)

### **Agent 4: Payments Engineer (InfinitePay)**
- **Must respect**: Constraints #1, #2, #10
- **No alternatives**: InfinitePay is mandate for MVP (#10)

---

## ⚠️ Common Violations & How to Handle

| Violation | Detection | Resolution |
|-----------|-----------|-----------|
| Agent suggests `localhost:3000` | Code contains `http://localhost` or `swa start` | Reject. Suggest Azure SWA CLI instead. |
| Agent creates mock data in schema | SQL has `INSERT` with test data, markers like `-- TEST` | Reject unless explicit fixture request. Real data only. |
| Agent proposes Flask/FastAPI | Backend uses non-Azure framework | Allow ONLY with documented trade-offs (cost, scaling, learning curve). Require approval. |
| Agent suggests gov API integration | Code calls SIGEF/CAR/FUNAI directly | Reject for MVP. Suggest WMS URL fallback. Document for phase 2. |
| Agent forgets SRID in geometry creation | SQL: `GEOMETRY(Polygon)` without `,4674` | Reject. Must be `GEOMETRY(Polygon, 4674)`. |
| Agent skips ST_IsValid checks | Schema lacks `CHECK (ST_IsValid(geom))` | Reject. Add constraint. |
| Agent creates >1 client per project | Schema design enforces one-to-one | Reject. Redesign to allow 1:N (already 6 tables support this). |

---

## 🚀 Escalation Path

**If constraint creates blocker**:
1. **Document** the specific constraint + why it blocks (provide example)
2. **Propose** alternative approach that respects spirit (e.g., "Can we use WMS URLs with caching?" instead of "Can we call gov APIs?")
3. **Escalate** to user for decision (only on HARD/MEDIUM constraints, never ABSOLUTE)

**Example escalation**:
> "Constraint #5 (Azure Functions only) blocks Agent 2 because FastAPI's async middlewares are superior to Functions runtime. Proposal: Use Flask Blueprints + ASGI adapter, still runs on Functions. Trade-off: +2hrs setup, better code organization. Approve?"

---

## 📝 Environment Status Checklist

**Currently Set** ✅:
- [x] `.github/copilot-instructions.md` (master guide)
- [x] `.agents/agent-1-data-engineer/AGENT_INSTRUCTIONS.md` (detailed mission)
- [x] `.agents/agent-1-data-engineer/run.py` (executor)
- [x] `.agents/agent-1-data-engineer/queries.sql` (validation)

**Awaiting User/Setup** ⏳:
- [ ] `DATABASE_URL` (Azure Database PostgreSQL connection string) → Needed before Agent 1 schema creation
- [ ] `OPENROUTER_API_KEY` (already uploaded, optional for Jamba code generation)
- [ ] `INFINITEPAY_API_KEY` (stand-by until Agent 4 needed)
- [ ] `JWT_SECRET` (random string for token signing) → Generate before Agent 2 backend

**Not Agents' Job** ℹ️:
- Azure Database PostgreSQL deployment (Agent 1 creates SQL, ops deploys to Azure)
- Node/Python installation (assumed pre-installed)
- Secrets management (ops/Azure Portal responsibility)

