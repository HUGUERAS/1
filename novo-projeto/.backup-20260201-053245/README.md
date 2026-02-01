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

## 🚀 Desenvolvimento (Cloud-First)

**⚠️ ATENÇÃO**: Este projeto NÃO usa localhost. Todo desenvolvimento é feito direto no Azure.

### Pré-requisitos
*   Conta Azure ativa
*   Azure CLI instalado (`az login`)
*   Git configurado

### Variáveis de Ambiente Necessárias
Configure no Azure Portal > Static Web Apps > Configuration:
*   `DATABASE_URL` - PostgreSQL connection string
*   `JWT_SECRET` - Token signing key
*   `INFINITEPAY_API_KEY` - Payment gateway key (opcional em desenvolvimento)
*   `OPENROUTER_API_KEY` - AI features key (opcional)

## ☁️ Deploy no Azure

### 1. Criar Azure Static Web App
```bash
az login
az staticwebapp create \
  --name ativo-real-prod \
  --resource-group seu-resource-group \
  --source https://github.com/seu-usuario/seu-repo \
  --location "East US 2" \
  --branch main \
  --app-location "ativo-real" \
  --api-location "backend" \
  --output-location "dist"
```

### 2. Configurar Variáveis de Ambiente
No Azure Portal:
1. Navegue para sua Static Web App
2. Settings > Configuration
3. Adicione as Application Settings necessárias (veja seção acima)

### 3. Deploy Automático
Cada push para `main` dispara deploy automático via GitHub Actions.

### 4. Criar Banco de Dados PostgreSQL
```bash
az postgres flexible-server create \
  --name ativo-real-db \
  --resource-group seu-resource-group \
  --location "East US 2" \
  --admin-user dbadmin \
  --admin-password "SuaSenhaSegura123!" \
  --sku-name Standard_B1ms \
  --version 14 \
  --storage-size 32
```

Depois rode o schema:
```bash
psql -h ativo-real-db.postgres.database.azure.com -U dbadmin -d postgres -f database/init/01_schema.sql
```

## 📁 Estrutura de Pastas

**Frontend Principal**: `ativo-real/` (React + TypeScript + Ant Design)  
**Backend**: `backend/` (Azure Functions v2 + Python)  
**Database**: `database/init/` (SQL scripts PostGIS)
