# 🔑 Environment & API Setup Checklist

**Last Updated**: 31/01/2026  
**Status**: Ready for Agent 1, awaiting environment configuration

---

## 📊 Setup Status Matrix

| Component | Required? | Status | Blocker? | Notes |
|-----------|-----------|--------|----------|-------|
| **DATABASE_URL** | ✅ YES | ⏳ Pending | 🔴 Yes | Azure Database for PostgreSQL connection string. Format: `postgresql://user:pass@server.postgres.database.azure.com/dbname?sslmode=require`. Blocks Agent 1 SQL execution. |
| **OPENROUTER_API_KEY** | ❓ Optional | ✅ Already uploaded | ⚪ No | For Jamba code generation (dev tool, VS Code only). Already configured. Can retrieve backup if needed. |
| **INFINITEPAY_API_KEY** | ✅ YES | ⏳ Stand-by | 🟡 Partial | Payment gateway key. Needed for Agent 4 (Payments). Currently in stand-by; can proceed with Agents 1-3 first. |
| **JWT_SECRET** | ✅ YES | ❌ Not set | 🟡 Partial | Token signing secret for auth_middleware.py. Needed for Agent 2 (Backend). Generate: `openssl rand -hex 32` or `secrets.token_hex(32)` in Python. |
| **Node.js** | ✅ Assumed | ℹ️ Pre-installed | ⚪ No | Must exist in Azure Functions runtime. NOT agent-installable. |
| **Python** | ✅ Assumed | ℹ️ Pre-installed | ⚪ No | Must exist in Azure Functions runtime. NOT agent-installable. |
| **PostgreSQL Client** | ❓ Optional | ℹ️ For testing | ⚪ No | For local schema testing (Agent 1 validation). Install `psql` if doing local testing (not required for cloud deployment). |
| **Azure Functions Core Tools** | ❓ Optional | ℹ️ For local testing | ⚪ No | For local Function testing. NOT needed (cloud-first dev). If needed: `npm install -g azure-functions-core-tools@4 --unsafe-perm true`. |

---

## ☁️ Azure Runtime (Node/Python) — How to “Install”

You do **not** install Node.js or Python manually in Azure. You **select the runtime stack** and Azure provisions it.

### **Azure Functions (Backend)**
1. Azure Portal → Function App → **Configuration** → **General settings**
2. Set **Runtime stack** = Python (3.x)
3. Set **Functions runtime version** = v4
4. Save, then restart the Function App

### **Azure Static Web Apps (Frontend)**
- The build pipeline chooses Node via config:
   - GitHub Actions workflow: `node-version: '20.x'` (recommended)
   - Or set in SWA build config if using Oryx

**Note**: This is the supported way to “install” Node/Python in Azure. Agents should not try OS-level installs.

---

## 🔴 Blockers for Agent Progress

### **Agent 1 (Database) - BLOCKED** 🔴
**Reason**: DATABASE_URL not configured  
**What Agent 1 can do**: 
- ✅ Generate SQL scripts (`.agents/agent-1-data-engineer/queries.sql` ready)
- ✅ Document schema constraints
- ✅ Create fixtures template

**What Agent 1 CANNOT do**:
- ❌ Execute SQL against database (no connection string)
- ❌ Validate schema in real PostgreSQL (no connection)
- ❌ Test PostGIS operations (no database)

**How to unblock**: 
1. Create Azure Database for PostgreSQL (if not exists)
2. Get connection string from Azure Portal
3. Set `DATABASE_URL` in Azure Portal > Application Settings
4. Or: `export DATABASE_URL="postgresql://..."` locally (for testing only)

---

### **Agent 2 (Backend) - PARTIALLY BLOCKED** 🟡
**Reason**: JWT_SECRET not generated  
**What Agent 2 can do**:
- ✅ Generate Azure Function boilerplate
- ✅ Create route structure (function_app.py)
- ✅ Design validation logic (logic_services.py)
- ✅ Build Pydantic schemas

**What Agent 2 CANNOT do**:
- ❌ Create auth_middleware.py (needs JWT_SECRET for token creation)
- ❌ Test authentication decorators (no secret)

**How to unblock**:
1. Generate JWT_SECRET: `python -c "import secrets; print(secrets.token_hex(32))"`
2. Example: `jwt_secret_key = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"`
3. Set in Azure Portal > Application Settings > `JWT_SECRET`
4. Add to `.env` if local testing: `JWT_SECRET=<value>`

---

### **Agent 3 (Frontend) - NOT BLOCKED** ✅
**Reason**: No environment variables needed for React development  
**Can proceed immediately with**:
- Component scaffolding
- OpenLayers integration
- Form building
- Map UI design

---

### **Agent 4 (Payments) - STAND-BY** 🟡
**Reason**: INFINITEPAY_API_KEY not required yet  
**Can proceed only after Agent 2 deploys** (need webhook endpoint)  
**When needed**:
1. Request InfinitePay API key from provider
2. Set in Azure Portal > Application Settings > `INFINITEPAY_API_KEY`
3. Whitelist webhook URL: `https://<swa-url>/api/payments/infinitepay`

---

## 🛠️ Quick Setup Instructions

### **Option 1: Azure Portal Setup (Recommended for Production)**

```bash
# In Azure Portal:
1. Go to: Azure Database for PostgreSQL > Connection strings
2. Copy "psql" or "Python" connection string
3. Go to: Static Web App > Application Settings
4. Add new setting:
   - Name: DATABASE_URL
   - Value: postgresql://user:pass@server.postgres.database.azure.com/dbname?sslmode=require
   
5. Generate JWT_SECRET locally:
   python -c "import secrets; print(secrets.token_hex(32))"
   
6. Add new setting:
   - Name: JWT_SECRET
   - Value: <generated-value>

7. Save
8. Restart Static Web App
```

### **Option 2: Local Testing with `.env` (For Development)**

```bash
# File: novo-projeto/.env
DATABASE_URL=postgresql://user:pass@localhost:5432/ativo_real_dev
JWT_SECRET=your-generated-secret-here
INFINITEPAY_API_KEY=test-key-placeholder
OPENROUTER_API_KEY=<already-uploaded-in-vs-code>
```

```bash
# Then in terminal:
cd novo-projeto/backend
pip install python-dotenv
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('DB:', os.getenv('DATABASE_URL'))"
```

### **Option 3: Environment Variables via CLI**

```bash
# Using Azure CLI:
az staticwebapp appsettings set --name <app-name> --setting-names DATABASE_URL=postgresql://... JWT_SECRET=...

# Using func (Azure Functions):
func azure functionapp publish <function-app-name> --build remote
func settings add DATABASE_URL "postgresql://..."
func settings add JWT_SECRET "..."
```

---

## 🧪 Validation Commands

### **Test DATABASE_URL Connection** ✅
```bash
# Using psql (if installed):
psql "$DATABASE_URL" -c "SELECT 1;"

# Using Python:
python -c "
import psycopg2
import os
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
print('✅ PostgreSQL connected')
conn.close()
"
```

### **Test JWT_SECRET Generation** ✅
```bash
python -c "
import secrets
import jwt
import os

secret = os.getenv('JWT_SECRET', secrets.token_hex(32))
payload = {'user_id': 1, 'role': 'TOPOGRAFO'}
token = jwt.encode(payload, secret, algorithm='HS256')
decoded = jwt.decode(token, secret, algorithms=['HS256'])
print(f'✅ JWT working: {decoded}')
"
```

### **Test OPENROUTER_API_KEY** ✅
```bash
# Check if key is in VS Code environment:
# 1. Open .agents/agent-1-data-engineer/run.py
# 2. Should reference: OPENROUTER_API_KEY from environment
# 3. Key already configured in Copilot session
```

---

## 🚀 Agent Execution Order

**To maximize progress without blockers**:

1. **Start Agent 3 (Frontend)** ✅ No blockers
   - Generate React components
   - Build OpenLayers map
   - Create form layouts

2. **Unblock Agent 1 (Database)** 🔓
   - Set DATABASE_URL
   - Run Agent 1 schema generation
   - Execute validation queries

3. **Unblock Agent 2 (Backend)** 🔓
   - Generate JWT_SECRET
   - Create Azure Functions boilerplate
   - Deploy to Azure (get endpoint URL)

4. **Start Agent 4 (Payments)** (when ready)
   - Get INFINITEPAY_API_KEY
   - Create webhook handler
   - Integrate with Agent 2 endpoints

---

## ❌ Common Issues & Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| **DATABASE_URL not set** | `psycopg2.OperationalError: could not connect` | Check Azure Portal > Application Settings > DATABASE_URL. Format must be exact. |
| **JWT_SECRET missing** | `NameError: 'jwt_secret_key' is not defined` | Generate: `python -c "import secrets; print(secrets.token_hex(32))"`. Set in Application Settings. |
| **Wrong SRID in schema** | PostGIS error: `could not find spatial_ref_sys row` | Check Agent 1 SQL: must use `4674`, not `4326`. Run: `SELECT * FROM spatial_ref_sys WHERE srid = 4674;` |
| **psycopg2 not installed** | `ModuleNotFoundError: No module named 'psycopg2'` | Agent 1/2 depend on this. Ensure `pip install -r requirements.txt` was run. |
| **OPENROUTER_API_KEY not found** | Code fails to use Jamba/Copilot for code gen | Key is already uploaded in VS Code session. If lost, request new one from OpenRouter dashboard. |

---

## 📝 Checklist for Ready State

Before declaring environment "READY FOR AGENTS":

- [ ] DATABASE_URL set in Azure Portal Application Settings
- [ ] PostgreSQL can be queried: `SELECT 1;` returns success
- [ ] JWT_SECRET generated and stored in Application Settings
- [ ] INFINITEPAY_API_KEY obtained (can be placeholder/test key for now)
- [ ] OPENROUTER_API_KEY confirmed in VS Code (already done)
- [ ] `.env` file created for local testing (optional)
- [ ] `novo-projeto/backend/requirements.txt` includes: `psycopg2-binary`, `pydantic`, `SQLAlchemy`, `geoalchemy2`, `shapely`

**Once all checked**: ✅ Agents can proceed with full execution

---

## 🎯 Next Steps

1. **Immediate** (5 min): Generate JWT_SECRET, set DATABASE_URL
2. **Short-term** (30 min): Validate database connection, run Agent 1 queries
3. **Medium-term** (next session): Deploy Agent 1 schema to Azure, start Agent 2
4. **Later**: Get INFINITEPAY_API_KEY when Agent 4 ready

**Questions?** Check `.agents/README.md` or `.agents/CONSTRAINTS.md`

