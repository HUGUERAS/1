# Ativo Real - GeoPlatform 🌍

Plataforma de gestão fundiária e topografia com validação geométrica inteligente.

## 🏗️ Arquitetura (Azure Native)

Este projeto foi reestruturado para ser Cloud-Native, utilizando o melhor do ecossistema Azure para performance e baixo custo.

*   **Frontend**: React + OpenLayers (Hospedado no **Azure Static Web Apps**)
*   **Backend**: Python Serverless (**Azure Functions v2**)
*   **Banco de Dados**: PostgreSQL com PostGIS (**Azure Database for PostgreSQL**)

### 🛡️ Diferenciais de Engenharia

1.  **Validação Geométrica no Backend**: O Frontend é apenas para desenho. A matemática pesada (interseções, sobreposições) é feita no Python usando `Shapely` e `GeoAlchemy2` antes de salvar no banco.
2.  **Topologia Rígida**: O banco de dados (PostGIS) possui constraints `CHECK(ST_IsValid(geom))` para impedir dados corrompidos.
3.  **Separação de Preocupações**:
    *   `frontend/`: Apenas visualização e captura de input.
    *   `backend/logic_services.py`: Regras de negócio puras (testáveis).
    *   `backend/function_app.py`: Camada de adaptação HTTP (Azure Functions).

## 📂 Estrutura do Projeto

```
novo-projeto/
├── backend/                  # Azure Functions (Python)
│   ├── function_app.py       # Entrypoint da API
│   ├── logic_services.py     # Lógica de Negócios (Validação de Sobreposição)
│   ├── models.py             # Modelos de Banco (SQLAlchemy)
│   └── tests/                # Testes Unitários
├── frontend/                 # React App (Vite)
│   ├── src/components/MapEditor.jsx  # Editor com OpenLayers e Snap
│   └── staticwebapp.config.json      # Configuração de Rotas do Azure
└── database/                 # Scripts SQL
    └── init/01_schema.sql    # Schema PostGIS inicial
```

## 🚀 Como Rodar Localmente

### Pré-requisitos
*   Node.js 18+
*   Python 3.11+
*   Azure Functions Core Tools (`npm i -g azure-functions-core-tools@4`)
*   Azure Static Web Apps CLI (`npm i -g @azure/static-web-apps-cli`)
*   PostgreSQL com PostGIS instalado localmente

### 1. Configurar Banco de Dados
Crie um banco local chamado `ativoreal_geo` e rode o script `database/init/01_schema.sql`.

### 2. Iniciar Aplicação Híbrida (Front + Back)
Na raiz do projeto (`novo-projeto`), rode:

```bash
swa start frontend --api-location backend
```

Isso vai iniciar:
*   Frontend em `http://localhost:4280`
*   Backend em `http://localhost:7071`
*   Proxy de API em `http://localhost:4280/api`

> **Nota**: Certifique-se de configurar a variável de ambiente `DATABASE_URL` no terminal onde for rodar o comando, ou crie um `local.settings.json` na pasta `backend`.

## ☁️ Deploy no Azure

1.  Crie um recurso **Azure Static Web Apps** no portal.
2.  Conecte ao seu repositório GitHub.
3.  Nas configurações de Build:
    *   **App Location**: `frontend`
    *   **Api Location**: `backend`
    *   **Output Location**: `dist`
4.  Configure as "Application Settings" no Portal do Azure com sua `DATABASE_URL` do PostgreSQL de produção.
