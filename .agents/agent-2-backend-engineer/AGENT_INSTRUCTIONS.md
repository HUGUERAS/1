# Agent 2: Backend Engineer - Azure Functions

## Mission
Review, validate, and enhance the existing Python Azure Functions backend (`novo-projeto/backend/`) to ensure:
1. Compliance with copilot-instructions.md (no localhost, no mocks, cloud-first)
2. Proper error handling, logging, and security
3. Integration with Agent 1 schema (PostgreSQL database)
4. All business logic in `logic_services.py` (not in function_app.py)
5. Pydantic validation in `schemas.py`
6. JWT auth with role-based access control

## Deliverables
1. **Backend Review Report**: Current state, issues, recommendations
2. **Enhanced function_app.py**: Verified endpoints with proper error handling
3. **Updated requirements.txt**: All dependencies with versions
4. **Auth Tests**: Verify JWT token flow works with Agent 1 schema

## Key Endpoints to Verify
- POST `/api/auth/login` - Authenticate users
- POST `/api/auth/refresh` - Refresh JWT token
- GET `/api/projects` - List user's projects (role-based)
- POST `/api/projects` - Create new project
- GET `/api/projects/{id}/lots` - List lots in project
- POST `/api/projects/{id}/lots` - Create lot with magic link
- GET `/api/lots/{token}/details` - Client portal access
- POST `/api/payments/infinitepay` - Payment webhook

## Constraints from copilot-instructions.md
- ❌ NO localhost ever
- ❌ NO mocks - real Azure services only
- ✅ Cloud-first: Azure Functions + Static Web Apps
- ✅ DB truth engine: PostGIS + Shapely validation (fallback to SQL-only for Azure)
- ✅ Role enforcement: TOPOGRAFO vs CLIENTE
- ✅ Magic links: 7-day expiry tokens

## Integration Points
1. **Database**: SQLAlchemy ORM → Agent 1 schema
2. **Geometry**: Shapely for validation → JSONB storage (PostGIS not available)
3. **Payments**: InfinitePay API integration
4. **Logging**: Azure Application Insights
5. **Auth**: JWT with RS256 signing (env: JWT_SECRET)

## Testing
After review, verify with Azure CLI:
```bash
func start  # Run locally for testing only
# Then deploy to Azure Static Web App
```
