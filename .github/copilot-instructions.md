# Copilot Instructions for Ativo Real

This file guides GitHub Copilot on the specific architecture, workflows, and conventions of the **Ativo Real** project.

## 🛑 CRITICAL USER CONSTRAINTS (READ FIRST)

1.  **NO LOCAL EXECUTION**: The local environment is unstable. **DO NOT** suggest running `swa start`, `func start`, or "testing locally". Assume the user will deploy to Azure to test changes. Focus on generating correct, production-ready code for the cloud environment.
2.  **PRESERVE EXISTING PAGES**: Do **NOT** delete, disconnect, or simplify existing pages (`src/pages/*`) or components without explicit permission. When refactoring `App.tsx`, preserve existing routing/navigation logic unless instructed otherwise. **NEVER** replace a multi-page routing system with a single-file component unless explicitly asked.

## 🏗️ Architecture & "Big Picture"

Ativo Real is a cloud-native **GeoPlatform** for land management and topography, designed for **Azure**.

*   **Architecture Style**: Azure Native Serverless.
*   **Frontend**: React (Vite) + OpenLayers (Maps) hosted on **Azure Static Web Apps**.
*   **Backend**: Python (**Azure Functions v2**) acting as an API.
*   **Database**: PostgreSQL with **PostGIS** extension (Azure Database for PostgreSQL), critical for spatial validation.
*   **Infrastructure**: Bicep (Infrastructure as Code).

**Key Design Principle**: 
*   **Frontend is for visualization/input**: Use `OpenLayers` to capture geometries.
*   **Backend is for truth/validation**: All complex geometric math (overlaps, intersections) happens in Python using `Shapely` and `GeoAlchemy2`.
*   **Strict Topology**: The database enforces validity via `ST_IsValid` constraints.

## 📂 Project Structure & Key Files

The project is monorepo-like inside `novo-projeto/`:

*   **Frontend** (`novo-projeto/ativo-real/`):
    *   `src/components/MapEditor.tsx`: Main map component using OpenLayers.
    *   `src/`: React components (Tailwind CSS).
    *   `src/pages/`: Contains critical application pages (Login, Dashboards). **Do not delete.**
    *   `staticwebapp.config.json`: Azure SWA routing configuration.
*   **Backend** (`novo-projeto/backend/`):
    *   `function_app.py`: Azure Functions entry point (Routes defined here).
    *   `logic_services.py`: **CRITICAL**. Contains pure business logic and geometric validation. Keep this decoupled from HTTP layers.
    *   `models.py`: SQLAlchemy ORM definitions.
    *   `schemas.py`: Pydantic models for request/response validation.
*   **Database** (`novo-projeto/database/`):
    *   `init/01_schema.sql`: Source of truth for database schema. **Do not rely on ORM auto-creation**, use SQL scripts.

## 💻 Deployment Workflow (Cloud First)

*   **Deployment**: The primary workflow is deploying to Azure Static Web Apps.
*   **Environment**: The code runs in Azure Functions (Linux) and uses Azure Database for PostgreSQL.
*   **Dependencies**: Ensure `requirements.txt` and `package.json` are always up-to-date for the build server.

## 📝 Coding Conventions

*   **Python (Backend)**:

## 📝 Coding Conventions

*   **Python (Backend)**:
    *   **Validation**: Use `pydantic` heavily for data validation.
    *   **ORM**: Use `SQLAlchemy` 2.0+ style.
    *   **Geo**: Use `shapely` for geometric operations and `geoalchemy2` for DB interactions.
    *   **Session Management**: Use `SessionLocal` pattern. ensuring `db.close()` in `finally` blocks (or context managers).
*   **TypeScript (Frontend)**:
    *   **Maps**: Prefer `ol` (OpenLayers) for map interactions.
    *   **Styling**: Use Tailwind CSS utility classes.
    *   **State**: React Hooks.

## 🔗 Integrations

*   **MCP Servers**: Located in `novo-projeto/mcp-servers/`.
*   **Payments**: InfinitePay integration (referenced in documentation).

## ⚠️ Common Pitfalls

*   **ORM vs SQL**: We use SQL scripts (`database/init/`) for schema definition, not `metadata.create_all()`.
*   **GeoJSON Handling**: Ensure standard GeoJSON format when passing data between Front/Back.
*   **Snap**: Frontend map editor implements snapping to ensuring topology consistency before sending to backend.
