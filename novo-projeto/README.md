# Ativo Real - GeoPlatform 🌍

Plataforma de gestão fundiária e topografia com validação geométrica inteligente.

## 🏗️ Arquitetura (Azure Native - Cloud-First)

**⚠️ IMPORTANTE**: Este projeto NÃO usa localhost. Todo desenvolvimento é feito direto no Azure.

* **Frontend**: React + TypeScript + Ant Design + OpenLayers → **Azure Static Web Apps**
* **Backend**: Python Serverless (Azure Functions v2)
* **Banco de Dados**: PostgreSQL + PostGIS (Azure Database for PostgreSQL)

### 🛡️ Diferenciais

1. **Validação Geométrica no Backend**: Matemática pesada (Shapely + GeoAlchemy2)
2. **Topologia Rígida**: Constraints `CHECK(ST_IsValid(geom))`
3. **Single-Page Application**: Cliente vê tudo em 1 página só (7 abas)

## 📂 Estrutura

```
novo-projeto/
├── ativo-real/              ✅ FRONTEND OFICIAL (React + TS)
│   └── src/
│       ├── components/      → ClientPortal (SINGLE PAGE)
│       ├── pages/           → LoginPage, Dashboards
│       └── App.tsx          → Rotas: / | /dashboard | /client/:token
├── backend/                 ✅ BACKEND OFICIAL (Azure Functions)
├── database/                ✅ SQL SCRIPTS (PostGIS)
├── frontend-legacy/         ⚠️  IGNORAR (versão antiga)
├── .archive/                📦 Docs históricos
├── README.md               📖 Este arquivo
├── ARCHITECTURE_SPECS.md   🏗️  Referência técnica
└── PROJECT_STATUS.md       📊 Status atual
```

## 🚀 Deploy no Azure (Único Método)

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

### 2. Criar PostgreSQL

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

### 3. Configurar Variáveis (Azure Portal)

| Variável | Obrigatório |
|----------|-------------|
| `DATABASE_URL` | ✅ Sim |
| `JWT_SECRET` | ✅ Sim |
| `OPENROUTER_API_KEY` | ⚠️ Opcional |
| `INFINITEPAY_API_KEY` | ⚠️ Opcional |

### 4. Deploy Automático

```bash
git push origin main
# GitHub Actions → Deploy automático
```

## 🎯 Fluxo de Trabalho

1. **Desenvolver** → Editar código localmente
2. **Commitar** → `git add . && git commit -m "feat: nova funcionalidade"`
3. **Deployar** → `git push origin main`
4. **Testar** → Acessar `https://seu-app.azurestaticapps.net`

## 📊 Status

Ver **PROJECT_STATUS.md**

**Resumo**:

* ✅ Backend: 90% (12 endpoints, JWT, AI, PostGIS)
* ✅ Frontend: 85% (Single-page client, dashboards)
* ✅ Database: 100% (Schema completo)

## 📚 Documentação

* **PROJECT_STATUS.md** - O que está pronto
* **ARCHITECTURE_SPECS.md** - Decisões técnicas
* **.agents/CONSTRAINTS.md** - Regras absolutas

---

**Desenvolvido 100% Cloud-Native com Azure** 🚀
