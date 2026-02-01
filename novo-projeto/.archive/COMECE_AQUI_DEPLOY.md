# 🎯 INICIANDO DEPLOY - CHECKLIST RÁPIDO

Você está prestes a fazer deploy no Azure! Aqui está o que vai acontecer:

---

## ✅ O QUE SERÁ CRIADO NO AZURE

| Recurso | Nome | Custo/Mês |
|---------|------|-----------|
| Resource Group | rg-ativo-real | Grátis |
| PostgreSQL | ativo-real-db-XXXX | ~$30 |
| Database | ativo_real | Incluído |
| Storage Account | ativorealstorage | ~$1 |
| Function App | ativo-real-backend | ~$0-5 |
| **TOTAL** | | **~$31-36/mês** |

---

## 🚀 DUAS FORMAS DE FAZER DEPLOY

### **OPÇÃO 1: Script Automático (MAIS FÁCIL)** ⭐

**Execute:**

```cmd
deploy_backend.bat
```

**O script vai:**

1. ✅ Verificar pré-requisitos (Azure CLI, Git, Node)
2. ✅ Fazer login no Azure
3. ✅ Criar Resource Group
4. ✅ Criar PostgreSQL Server (~3 min)
5. ⚠️ Pedir para você executar SQL manualmente (Azure Portal)
6. ✅ Criar Function App
7. ✅ Configurar variáveis de ambiente
8. ✅ Fazer deploy do backend (~2 min)

**Tempo total:** ~10 minutos

---

### **OPÇÃO 2: Manual (Comandos)**

Siga o arquivo: `DEPLOY_EXPRESS.md`

Cole os comandos um por um no terminal.

---

## ⚠️ IMPORTANTE ANTES DE COMEÇAR

### **1. Você tem Azure CLI instalado?**

```cmd
az --version
```

❌ **Se não tiver, instale:**
<https://aka.ms/azure-cli>

### **2. Você tem conta Azure ativa?**

- Vá em: <https://portal.azure.com>
- Confirme que consegue fazer login

### **3. Você tem GitHub conta?**

- Frontend será deployado via GitHub Actions
- Você vai precisar criar um repositório

---

## 📊 APÓS O DEPLOY DO BACKEND

Você terá:

- ✅ **Backend rodando:** `https://ativo-real-backend-XXXX.azurewebsites.net/api`
- ✅ **8 endpoints funcionando:**
  - POST/GET /wms-layers
  - POST/GET /chat/messages
  - GET /lotes/{id}/status-history
  - GET /auth/magic-link/{token}
  - PATCH/DELETE /wms-layers/{id}

---

## 🌐 DEPLOY DO FRONTEND (DEPOIS)

Após backend deployado:

1. Criar repositório GitHub
2. Push do código
3. Criar Static Web App
4. GitHub Actions fará deploy automático

**(Também tem script para isso: `deploy_frontend.bat`)**

---

## 🐛 SE DER ERRO

### **Erro: "Name already exists"**

- Nomes no Azure precisam ser únicos globalmente
- Script adiciona número aleatório automaticamente
- Se falhar, tente novamente

### **Erro: "Subscription not found"**

- Execute: `az account list`
- Escolha a subscription correta
- Execute: `az account set --subscription "Nome-da-Subscription"`

### **Erro: "Insufficient permissions"**

- Você precisa ser **Contributor** ou **Owner** da subscription
- Fale com o administrador da conta Azure

---

## 💰 CUSTOS PREVISTOS

- **Primeiro mês:** ~$31-36 USD
- **Após 12 meses:** Verificar tier do PostgreSQL (pode subir)
- **Dica:** Pause recursos quando não estiver usando

---

## 🎯 ESTÁ PRONTO?

### **Para começar:**

```cmd
deploy_backend.bat
```

### **Ou siga passo a passo:**

```cmd
DEPLOY_EXPRESS.md
```

---

## 📝 ARQUIVOS QUE SERÃO DEPLOYADOS

### **Backend (Python):**

- ✅ function_app.py - 8 endpoints novos
- ✅ logic_services.py - Validações PostGIS
- ✅ models.py - 4 models novos
- ✅ requirements.txt - Dependências

### **Database:**

- ✅ 05_features_completas.sql - 4 tabelas novas

**Total:** ~800 linhas de código backend

---

## ✅ CHECKLIST PRÉ-DEPLOY

- [ ] Azure CLI instalado
- [ ] Conta Azure ativa
- [ ] Cartão de crédito vinculado (para custos)
- [ ] GitHub conta criada
- [ ] Ler custos estimados (~$35/mês)
- [ ] Backup do código feito

---

**PRONTO PARA COMEÇAR?** Execute `deploy_backend.bat` 🚀

**OU** siga `DEPLOY_EXPRESS.md` para comandos manuais

---

**DÚVIDAS?**

- Consulte: `DEPLOY_AZURE_DIRETO.md` (guia completo)
- Consulte: `IMPLEMENTACAO_FINAL_COMPLETA.md` (documentação técnica)
