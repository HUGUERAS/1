# GitHub Copilot Instructions - Ativo Real

## 🏗 Project Architecture
- **Hybrid Monorepo**: React frontend (`src/`) + Python Azure Functions backend (`api/`).
- **Database**: Azure Database for PostgreSQL (Flexible Server) with **PostGIS** extension.
- **Frontend**: React 19 + TypeScript + Vite.
- **Backend**: Azure Functions (Python v2 Model). Defined in `api/function_app.py`.

## 🚀 Development Workflow
- **Frontend**: `npm run dev`
- **Backend (Python)**:
  1. `cd api`
  2. Create/Activate virtual env: `python -m venv .venv`, `.\.venv\Scripts\activate`
  3. Install deps: `pip install -r requirements.txt`
  4. Run: `func start`
- **Env Vars**:
  - `VITE_API_BASE=http://localhost:7071/api` (Frontend)
  - `POSTGRES_CONNECTION_STRING` in `api/local.settings.json` (Backend)

## 🧩 Key Patterns
- **Database Schema**: Managed in `database/schema.sql`. Use PostGIS geometries (`GEOMETRY(Polygon, 4326)`).
- **API (Python)**:
  - Uses `azure-functions` library (v2 model decorators).
  - Uses `psycopg2` for direct DB connection.


### Frontend (React + Maps)
- **Map Components**: Use `React-Leaflet`. Main view: `src/components/Map/MapView.tsx`.
- **Styling**: Mixed approach.
  - Utility classes: **Tailwind CSS**.
  - Complex components: **CSS Modules** (e.g., `MapView.css`, `LayerControl.css`).
- **State Management**: Local React state + Props.
- **API Service**: Centralized in `src/services/onboardingService.ts`. Use generic `postJson` wrapper.

### Data Types
- **GeoJSON**: Used for map layers. Parsed via `togeojson`.
- **Layer Interfaces**: Defined in `MapView.tsx` (`MarkerData`, `PolygonData`, `MapLayer`).

## ⚠️ Critical Files
- `functions.js`: Backend entry point. DO NOT DELETE.
- `src/functions/index.js`: Registers function handlers.
- `src/components/Map/MapView.tsx`: Core map logic and layer rendering.
- `local.settings.json`: Local backend settings (excluded from git).

## 🧪 Testing
- **Unit**: `npm test` (Vitest).
- **Manual**: Use `src/mocks/mockServer.js` or run full backend with `npm start` to test API flows.
