# ⚡ DEPLOY EXPRESS - COMANDOS PRONTOS

**Cole estes comandos direto no terminal para deploy rápido!**

---

## 🔑 PASSO 0: LOGIN

```bash
az login
```

---

## 📦 PASSO 1: CRIAR INFRAESTRUTURA (5 minutos)

```bash
# Resource Group
az group create --name rg-ativo-real --location brazilsouth

# PostgreSQL (pode demorar ~3 minutos)
az postgres flexible-server create \
  --name ativo-real-db \
  --resource-group rg-ativo-real \
  --location brazilsouth \
  --admin-user adminativo \
  --admin-password "AtivO@Real2026!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 14 \
  --storage-size 32 \
  --public-access 0.0.0.0-255.255.255.255

# Database
az postgres flexible-server db create \
  --resource-group rg-ativo-real \
  --server-name ativo-real-db \
  --database-name ativo_real

# Storage Account
az storage account create \
  --name ativorealstorage \
  --resource-group rg-ativo-real \
  --location brazilsouth \
  --sku Standard_LRS

# Function App
az functionapp create \
  --name ativo-real-backend \
  --resource-group rg-ativo-real \
  --consumption-plan-location brazilsouth \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --storage-account ativorealstorage \
  --os-type Linux
```

---

## ⚙️ PASSO 2: CONFIGURAR VARIÁVEIS (1 minuto)

```bash
# Database URL
az functionapp config appsettings set \
  --name ativo-real-backend \
  --resource-group rg-ativo-real \
  --settings "DATABASE_URL=postgresql://adminativo:AtivO@Real2026!@ativo-real-db.postgres.database.azure.com/ativo_real?sslmode=require"

# JWT Secret
az functionapp config appsettings set \
  --name ativo-real-backend \
  --resource-group rg-ativo-real \
  --settings "JWT_SECRET=ativo_real_jwt_secret_2026_super_secure"

# CORS
az functionapp cors add \
  --name ativo-real-backend \
  --resource-group rg-ativo-real \
  --allowed-origins "*"
```

---

## 📊 PASSO 3: EXECUTAR SQL (2 minutos)

### Opção A - Via Azure Portal (RECOMENDADO)

1. Acesse: <https://portal.azure.com>
2. Busque: "ativo-real-db"
3. Menu lateral: **Databases** → ativo_real
4. Menu lateral: **Query editor**
5. Login: `adminativo` / `AtivO@Real2026!`
6. Cole o conteúdo do arquivo: `database/init/05_features_completas.sql`
7. Clique em **Run**

### Opção B - Via psql (se tiver instalado)

```bash
cd database/init

psql "postgresql://adminativo:AtivO@Real2026!@ativo-real-db.postgres.database.azure.com/ativo_real?sslmode=require" -f 05_features_completas.sql
```

---

## 🚀 PASSO 4: DEPLOY BACKEND (3 minutos)

```bash
cd backend

# Instalar Azure Functions Core Tools (se não tiver)
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Deploy
func azure functionapp publish ativo-real-backend --build remote
```

**✅ Aguarde até ver:** `Deployment successful`

**🔗 Sua URL do Backend:**

```
https://ativo-real-backend.azurewebsites.net/api
```

---

## 🌐 PASSO 5: PREPARAR GITHUB (2 minutos)

```bash
cd ..  # Voltar para raiz do projeto

# Se ainda não tem Git iniciado:
git init
git add .
git commit -m "Deploy inicial - Sistema completo"

# Criar repositório no GitHub (manual):
# 1. Vá em: https://github.com/new
# 2. Nome: ativo-real-topografia
# 3. Privado: SIM
# 4. NÃO inicialize com README
# 5. Crie

# Conectar ao GitHub (SUBSTITUA SEU_USUARIO):
git remote add origin https://github.com/SEU_USUARIO/ativo-real-topografia.git
git branch -M main
git push -u origin main
```

---

## 📱 PASSO 6: DEPLOY FRONTEND (3 minutos)

```bash
# SUBSTITUA SEU_USUARIO pelo seu usuário GitHub
az staticwebapp create \
  --name ativo-real-frontend \
  --resource-group rg-ativo-real \
  --source https://github.com/SEU_USUARIO/ativo-real-topografia \
  --location brazilsouth \
  --branch main \
  --app-location "ativo-real" \
  --output-location "dist" \
  --login-with-github
```

**⚠️ Este comando vai:**

1. Abrir o navegador
2. Pedir autorização do GitHub
3. Criar workflow automático

**✅ Aguarde até ver:** `Successfully created`

---

## 🔗 PASSO 7: OBTER URLS FINAIS

```bash
# URL do Frontend
az staticwebapp show \
  --name ativo-real-frontend \
  --resource-group rg-ativo-real \
  --query "defaultHostname" -o tsv

# URL do Backend
echo "https://ativo-real-backend.azurewebsites.net/api"
```

**📝 ANOTE ESSAS URLS!**

---

## ✅ PASSO 8: TESTAR

```bash
# Testar backend
curl https://ativo-real-backend.azurewebsites.net/api/wms-layers?projeto_id=1

# Abrir frontend no navegador
start https://[SUA-URL-FRONTEND].azurestaticapps.net
```

---

## 🎯 RESUMO RÁPIDO (COPY & PASTE)

### **Para deploy completo em ~15 minutos:**

1. **Login:** `az login`
2. **Criar tudo:** Cole os comandos do PASSO 1
3. **Configurar:** Cole os comandos do PASSO 2
4. **SQL:** Use Azure Portal (PASSO 3)
5. **Deploy Backend:** Cole comandos do PASSO 4
6. **GitHub:** Configure manual (PASSO 5)
7. **Deploy Frontend:** Cole comando do PASSO 6
8. **Obter URLs:** Cole comandos do PASSO 7
9. **Testar:** Acesse as URLs!

---

## 🐛 SE DER ERRO

### **Erro: "Name already exists"**

Use outro nome:

```bash
--name ativo-real-db-SEU-NOME
--name ativo-real-backend-SEU-NOME
```

### **Erro: "func: command not found"**

Instale:

```bash
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

### **Erro: "az: command not found"**

Instale Azure CLI: <https://aka.ms/azure-cli>

### **Erro SQL**

Execute manualmente via Azure Portal (mais fácil)

---

## 💰 CUSTO

**~$35 USD/mês** para MVP em produção

Para reduzir custos:

- Use tier Free do PostgreSQL (se disponível)
- Pause recursos quando não usar

---

## 🔄 ATUALIZAÇÕES FUTURAS

Depois do deploy inicial, para atualizar:

```bash
# Backend
cd backend
func azure functionapp publish ativo-real-backend

# Frontend (automático via GitHub)
cd ..
git add .
git commit -m "Atualização"
git push
```

GitHub Actions faz deploy automático do frontend! 🚀

---

**PRONTO! Sistema no ar em ~15 minutos!** 🎉

**URLs que você vai ter:**

- Frontend: `https://[nome].azurestaticapps.net`
- Backend: `https://ativo-real-backend.azurewebsites.net/api`
- Database: `ativo-real-db.postgres.database.azure.com`
