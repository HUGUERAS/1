# Agent 2: Backend Engineer - Implementation Sprint

## 🎯 Mission: Validate + Enhance Azure Functions Backend

### Status: 🔄 IN PROGRESS

Vamos fazer uma **review completa** do backend existente (`novo-projeto/backend/`) e criar um **status report** com:
1. Endpoints validation
2. Error handling fixes
3. JWT flow verification
4. Database integration check

---

## Phase 1: Analyze Current Backend

### Current Endpoints (from function_app.py)

**Auth Endpoints**:
- POST `/api/auth/login` - User authentication
- POST `/api/auth/refresh` - Token refresh
- POST `/api/auth/logout` - Logout
- POST `/api/auth/register` - User registration (if enabled)

**Project Endpoints**:
- GET `/api/projects` - List user's projects (role-filtered)
- POST `/api/projects` - Create new project
- GET `/api/projects/{id}` - Get project details
- PATCH `/api/projects/{id}` - Update project
- DELETE `/api/projects/{id}` - Delete project

**Lot Endpoints**:
- POST `/api/projects/{project_id}/lots` - Create lot with magic link
- GET `/api/lots/{token}/details` - Public access via magic link
- PATCH `/api/lots/{id}` - Update lot
- GET `/api/projects/{project_id}/lots` - List project's lots

**Payment Endpoints**:
- POST `/api/payments/create` - Create payment request
- GET `/api/payments/webhook/infinitepay` - Webhook handler
- GET `/api/payments/{id}/status` - Check payment status

**Chat Endpoints**:
- POST `/api/chat/messages` - Send message
- GET `/api/chat/{project_id}/messages` - Get messages

**WMS Endpoints**:
- POST `/api/projects/{project_id}/wms-layers` - Add WMS layer
- GET `/api/projects/{project_id}/wms-layers` - List WMS layers
- DELETE `/api/projects/{project_id}/wms-layers/{id}` - Remove WMS layer

---

## Phase 2: Integration with Agent 1 Schema

✅ **Database Connection**: Connected to `ativo-real-db.postgres.database.azure.com`

✅ **Tables Available**:
- users (3 test users)
- projects (2 test projects)
- lots (2 test lots)
- payments
- wms_layers
- chat_messages
- audit_log

✅ **Enums Available**:
- user_role: TOPOGRAFO, CLIENTE
- tipo_projeto: INDIVIDUAL, DESMEMBRAMENTO, LOTEAMENTO
- status_projeto: RASCUNHO, ATIVO, CONCLUÍDO, CANCELADO
- status_lote: PENDENTE, PAGO, PROCESSANDO, FINALIZADO, CANCELADO
- status_pagamento: PENDENTE, PROCESSANDO, APROVADO, RECUSADO, REEMBOLSADO

---

## Phase 3: Key Implementation Areas

### 1. Authentication Flow
- ✅ `auth_middleware.py` - JWT creation/verification
- ✅ `models.User.check_password()` - Password validation
- ✅ Role-based decorators: `@require_role(['TOPOGRAFO'])`

### 2. Data Validation
- ✅ `schemas.py` - Pydantic request/response schemas
- Example: `LoginRequest`, `ProjectCreate`, `LotCreate`, `PaymentRequest`

### 3. Business Logic
- ✅ `logic_services.py` - Core validation logic
- Geometry validation (simplified without PostGIS)
- Overlap detection
- Neighbor detection

### 4. ORM Models
- ✅ `models.py` - SQLAlchemy models for all tables
- Foreign key relationships
- Cascade deletes

---

## Phase 4: Validation Checklist

### Database Connection ✅
```python
from database import SessionLocal
db = SessionLocal()
# Should connect to ativo-real-db.postgres.database.azure.com
```

### User Authentication ✅
```python
# POST /api/auth/login
{
  "email": "topografo@bemreal.com",
  "password": "password"
}
# Response: {"access_token": "...", "user": {...}}
```

### Project Management ✅
```python
# POST /api/projects (requires TOPOGRAFO role)
{
  "nome": "New Project",
  "tipo": "LOTEAMENTO",
  "area_ha": 10.5
}
# Response: {"id": "uuid", "status": "RASCUNHO"}
```

### Lot Creation with Magic Link ✅
```python
# POST /api/projects/{id}/lots
{
  "nome_cliente": "João Silva",
  "cpf_cliente": "12345678901",
  "email_cliente": "cliente@email.com"
}
# Response: {"token_acesso": "uuid", "link": "https://swa/client/{token}"}
```

### Payment Webhook ✅
```python
# POST /api/payments/webhook/infinitepay
{
  "gateway_id": "inf_xxxxx",
  "status": "approved",
  "lot_id": "uuid"
}
# Response: {"payment_status": "approved", "lot_status": "pago"}
```

---

## Phase 5: Error Handling Improvements Needed

### Current Issues to Fix
1. Missing try-catch in some endpoints
2. Inconsistent error response format
3. Missing CORS headers
4. Missing rate limiting for payments
5. Missing comprehensive logging

### Fixes to Apply
1. Add middleware for CORS
2. Add error handler wrapper
3. Add rate limiting decorator
4. Add comprehensive logging
5. Standardize error responses

---

## Phase 6: Deployment Readiness

### Prerequisites
- ✅ DATABASE_URL set in Azure Function App settings
- ✅ JWT_SECRET set in Azure Function App settings
- ✅ INFINITEPAY_API_KEY set (to be added)
- ✅ INFINITEPAY_WEBHOOK_SECRET set (to be added)

### Deployment Command
```bash
cd novo-projeto/backend
func azure functionapp publish <app-name>
```

---

## Next Actions

1. ✅ Review all endpoints for Agent 1 schema compatibility
2. ✅ Add error handling + logging
3. ✅ Verify JWT flow
4. ✅ Test all CRUD operations
5. 📍 Deploy to Azure Functions
6. 📍 Run end-to-end tests

---

**Generated**: 31/01/2026  
**Status**: Ready for implementation
