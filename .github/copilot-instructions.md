# Copilot Instructions for Ativo Real

Guides AI coding agents on architecture, workflows, and constraints for this **Topography SaaS** project.

## 🛑 ABSOLUTE RULES (Never Break These!)

1. **NO LOCALHOST EVER**: All development assumes Azure cloud deployment. Do NOT suggest `localhost:8000`, `swa start`, `func start`, or local testing. Production code only.

2. **NO MOCKS EVER**: Real integrations with real Azure services. No mock data, no mock APIs, no "development mode" with fake responses.

3. **Cloud-First Development**: Code must run in Azure Functions + Static Web Apps from day 1. Test by deploying to Azure, not locally.

## 🏗️ Architecture: Azure Serverless GeoPlatform

**Business Context**: Topographer creates "work orders" (projects) for land regularization. Each work can have 1+ clients (property owners). Clients access via unique link → single-page portal to fill forms, preview map, pay, track progress. Topographer does field surveying + generates technical documents (Memorial, Planta, Caderneta) for final delivery.

**Stack**: 
- Frontend: React (Vite) + OpenLayers → Azure Static Web Apps
- Backend: Python Azure Functions v2 (HTTP Triggers)
- Database: PostgreSQL + PostGIS (Azure Flexible Server)

**Design Principle**: 
- Frontend = Canvas for preview (simple draw tools, not CAD precision)
- Backend = Truth engine (Shapely + PostGIS for geometric validation)
- Database = Enforces topology (ST_IsValid, ST_Within constraints)

**Key Separation**:
- `function_app.py` = HTTP routing only
- `logic_services.py` = Pure business logic (decoupled, testable)
- `models.py` = SQLAlchemy ORM (schema defined by SQL scripts, not auto-create)

## 📂 Project Layout

```
novo-projeto/
├── ativo-real/                    # React + Vite frontend
│   ├── src/components/            
│   │   └── GlobalMap.tsx          # Main map (OpenLayers, Draw/Modify/Snap)
│   ├── src/pages/                 # Login, TopographerDashboard, ClientPortal
│   ├── src/services/              # API clients
│   ├── src/assets/                # Icons, logo, images (already implemented)
│   └── staticwebapp.config.json   # SWA routes
├── backend/                       # Python Azure Functions
│   ├── function_app.py            # HTTP endpoints (@app.route)
│   ├── logic_services.py          # CRITICAL: Geometric validation
│   ├── models.py                  # SQLAlchemy ORM
│   ├── schemas.py                 # Pydantic validators
│   ├── auth_middleware.py         # JWT tokens
│   ├── jamba_openrouter.py        # Internal dev tool (data analysis)
│   └── requirements.txt           
├── database/
│   └── init/
│       ├── 01_schema.sql          # Source of truth (projetos, lotes, pagamentos)
│       └── 04_users_auth.sql      # User roles (TOPOGRAFO, CLIENTE)
└── OPENROUTER_QUICKSTART.md       # Dev tool setup guide
```

## 🔄 Complete Business Flow

1. **Topographer Creates Work** → adds 1+ clients (name, CPF, email)
2. **Generates Magic Links** → JWT token UUID, 7-day expiry
3. **Client Accesses Single Page** via unique link:
   - Form (name, CPF, address, phone - standard registry data)
   - Map preview (simple draw polygon - visual reference only)
   - Contract view/download (PDF)
   - Payment (InfinitePay PIX/Card/Boleto)
   - File import/export (KML, GeoJSON, PDF, Excel)
   - Work tracking (status timeline)
   - Simple text chat with topographer
4. **Topographer Dashboard**:
   - Lists all projects (filter by status/client/date)
   - Sees multiple clients per work (normal use case, not exception)
   - Adds WMS layer URLs (SIGEF, CAR, FUNAI) for visualization
   - Controls layer visibility/opacity
   - Field surveying (external workflow)
   - Generates basic technical docs (Memorial, Planta, Caderneta)
   - Marks work as delivered
5. **End of Relationship** = Delivery of technical documents + project closed

## 🤖 Internal Dev Tools (VS Code Only - NOT Customer-Facing)

**OpenRouter Integration** (developer/backend analysis tool):
- **Where it runs**: Inside VS Code (your development environment)
- Provider: OpenRouter SDK (unified access to multiple LLMs)
- Models available:
  - Phi-Silica 3.6 (4K context, free) - quick code/data analysis
  - Jamba 1.7 Large (256K context, $0.40/1M) - deep analysis, schema review
- Use cases: 
  - Code generation assistance (backend logic, validators, migrations)
  - Data quality validation (internal auditing)
  - Schema analysis + documentation
  - Report preprocessing (internal only)
- Setup: See `OPENROUTER_QUICKSTART.md`, `backend/jamba_openrouter.py`
- **NEVER deployed to production** - dev environment only
- **NEVER exposed to users** - this is YOUR tool, not the product

## 🗺️ WMS Layers Pattern (Government Data Visualization)

**Important**: NOT API integration. Topographer manually adds URLs to visualize gov layers.

- Topographer inputs WMS URLs (SIGEF, CAR, FUNAI endpoints)
- System loads as OpenLayers TileLayer with WMS source
- Controls: visibility toggle, opacity slider
- Saved per project in `wms_layers` table (id, project_id, name, url, visible, opacity)

## 💻 Deployment & Environment

**Deploy**: Push to GitHub → SWA auto-builds (`App Location: ativo-real`, `API Location: backend`)

**Environment Variables**: Store in Azure Portal Application Settings:
- `DATABASE_URL` - PostgreSQL connection string
- `OPENROUTER_API_KEY` - For internal dev tools (optional)
- `INFINITEPAY_API_KEY` - Payment gateway
- `JWT_SECRET` - Token signing

**Build Backend**: `cd backend && pip install -r requirements.txt`

## 📝 Coding Conventions

**Python (Backend)**:
- Validation: Pydantic heavily (schemas.py)
- ORM: SQLAlchemy 2.0+ style
- Geo: Shapely (operations) + GeoAlchemy2 (DB types)
- Session: `SessionLocal` with `try/finally` cleanup
- Auth: JWT with `@require_auth`, `@require_role(['topographer'])`
- Async: Use `async/await` for Azure Functions HTTP triggers

**TypeScript (Frontend)**:
- Maps: OpenLayers (ol.Map, ol.interaction.Draw/Modify/Snap)
- **UI Libraries**: Material-UI (MUI), Ant Design, or other libraries allowed
- **Icons & Branding**: Use existing project icons + logo (already implemented in `src/assets/`)
- Styling: Tailwind CSS + component libraries + custom CSS-in-JS
- State: React Hooks + local component state (context for shared state if needed)
- File handling: KML (new KML()), Shapefile (shpjs library), GeoJSON
- API calls: Always use `/api/` prefix (SWA routing handles backend proxy)
@@- **Component architecture**: Keep individual features modular (15+ components is normal for complex UI with map, forms, controls). Avoid monolithic mega-components; split by responsibility.

## 🔐 Auth & Roles

**JWT Flow** (auth_middleware.py):
- `create_access_token(user_id, role)` → 30 min expiry
- Magic Links: UUID token in `lots.token_acesso` + `link_expira_em` (7 days)
- Decorators: `@require_auth`, `@require_role(['topographer'])`
- Roles: `TOPOGRAFO` (admin, creates projects) | `CLIENTE` (limited, own lot only)

## 🗺️ Spatial Validation (Backend Core)

**Flow**: Frontend draws WKT → Backend `logic_services.check_overlap_warnings(wkt, projeto_id, db)` → PostGIS queries

**Constants** (logic_services.py):
- `TOLERANCIA_SOBREPOSICAO_GRAUS = 0.0000001` (real overlap ~1cm²)
- `TOLERANCIA_SNAP_METROS = 0.5` (snap warning threshold)
- `SRID_OFICIAL = 4674` (SIRGAS 2000 CRS - mandatory for Brazil INCRA)

**PostGIS Operations**:
- `ST_Intersects()` - detect overlaps with neighbors/SIGEF
- `ST_Within()` - ensure lot inside project gleba
- `ST_IsValid()` - constraint on all geometries
- `ST_Touches()` - detect shared boundaries (confrontation)
- `ST_Area()` - calculate hectares (geodesic)

**Return**: Warnings (non-blocking) + `metadata_validacao` JSON with % overlap, neighbors, etc.

## 📋 Data Model (see 01_schema.sql)

Core tables:
- `users` (id, email, password_hash, role: TOPOGRAFO|CLIENTE)
- `projects` (id, nome, tipo: INDIVIDUAL|DESMEMBRAMENTO|LOTEAMENTO, status)
- `lots` (id, project_id, nome_cliente, token_acesso, geom POLYGON(4674), area_ha, status: PENDENTE→PAGO→FINALIZADO)
- `wms_layers` (id, project_id, name, url, visible, opacity)
- `payments` (id, lote_id, valor_total, status, gateway_id)
- `chat_messages` (id, project_id, sender_id, message, created_at)

**Important**: Multiple clients per project is the normal use case, not exception.

## 🚀 Integrations

- **InfinitePay**: POST `/api/payments/infinitepay` (webhook handler, async payment confirmation)
- **WMS Layers**: User-provided URLs (no API calls, just OpenLayers TileLayer visualization)
- **OpenRouter**: Internal backend tool for data analysis (not exposed to users)

## ⚠️ Anti-Patterns (Never Do This!)
@@- **Gov APIs (SIGEF/CAR/FUNAI)**: NO direct API integration in MVP. Visualization via WMS layer URLs only. **Fallback strategy**: If gov APIs fail, apply WMS URLs manually - do NOT block functionality due to external service unavailability. Future phases may add direct API integration.

 ❌ Single framework enforced (Flask, Django, FastAPI) → Azure Functions only, unless substantial architectural improvement justifies deviation (then document trade-offs)

## 🎯 Current Implementation Priorities

**Client Portal (Single Page)**: 
Form, map preview, contract view/download, payment, file import/export, status tracking, chat

**Topographer Dashboard**: 
Project list, multiple clients per work, WMS layer management, neighbor detection (PostGIS), basic doc generation, mark delivered

**Backend Endpoints**: 
Auth, Projects CRUD, Clients CRUD, Lots CRUD, WMS layers, Neighbors (PostGIS queries), Payments webhook, Chat

**Future Considerations** (not current priorities):
- CAD integration (Métrica Topo style automation)
- Gov API direct integration (currently WMS visualization only)
- Advanced reporting/analytics
- Mobile native app
@@- **Role-based visibility**: Topographer sees ONLY projects they created (not all system projects)
@@- **Token expiry**: 30 min default for sessions (customizable for specific workflows)
