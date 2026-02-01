# Agent 3: Frontend Engineer - React + Vite

## Mission
Review and enhance React/Vite frontend (`novo-projeto/ativo-real/`) to ensure:
1. Compliance with copilot-instructions.md
2. Proper integration with Agent 2 backend API
3. OpenLayers map component for geometry visualization
4. Client portal single-page access via magic token
5. Topographer dashboard with WMS layer management
6. File import/export (KML, GeoJSON, PDF, Excel)
7. Payment integration redirect to InfinitePay
8. Real-time chat with topographer

## Deliverables
1. **Frontend Review Report**: Current state, missing components, recommendations
2. **Enhanced Components**:
   - `GlobalMap.tsx` - OpenLayers map with Draw/Modify/Snap interactions
   - `ClientPortal.tsx` - Single-page for lot clients
   - `TopographerDashboard.tsx` - Project management UI
   - `WmsLayerManager.tsx` - Add/remove/control WMS layers
   - `PaymentRedirect.tsx` - InfinitePay integration
   - `ChatWidget.tsx` - Simple messaging UI
3. **API Service Layer**: Typed API client (`src/services/api.ts`)
4. **Build & Deploy**: Vite config for Static Web App

## Key Pages
1. **Login** (`/`) - Email/password for topographer
2. **Topographer Dashboard** (`/dashboard`) - Project list, create, manage
3. **Client Portal** (`/client/{token}`) - Form + map preview + payment + tracking
4. **Project Details** (`/dashboard/projects/{id}`) - Multiple clients, WMS layers, documents

## Constraints from copilot-instructions.md
- ❌ NO localhost testing - deploy to Azure SWA
- ❌ NO mocks - real API calls to Agent 2 backend
- ✅ OpenLayers for map visualization (not CAD precision)
- ✅ Simple draw tools (polygon, modify, snap)
- ✅ Geometry validation backend-only (send WKT to Agent 2)
- ✅ Role-based UI (TOPOGRAFO vs CLIENTE views)
- ✅ 7-day token expiry enforcement

## Integration Points
1. **API**: Calls Agent 2 backend at `/api/*` routes
2. **Map**: OpenLayers + WMS layers from database
3. **Auth**: JWT token stored in localStorage, refresh on 401
4. **Files**: KML, GeoJSON, PDF export via backend
5. **Payment**: Redirect to InfinitePay, webhook confirmation

## UI Components Library
- Material-UI (MUI) or Ant Design (already in project)
- Tailwind CSS for styling
- OpenLayers for maps
- Shapefile & KML libraries for file handling

## Testing
- Build: `npm run build`
- Deploy to SWA: Push to GitHub, auto-deploy
