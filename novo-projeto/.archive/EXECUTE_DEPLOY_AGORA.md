# ⚡ DEPLOY AGORA - COPIE E COLE ESTES COMANDOS

**Data:** 01/02/2026 05:56
**Status:** PRONTO PARA DEPLOY

---

## 🚀 PASSO A PASSO - COPIE E COLE

### **1. Abra o Prompt de Comando (cmd.exe)**

Pressione: `Win + R` → Digite: `cmd` → Enter

---

### **2. Navegue até a pasta do projeto:**

```cmd
cd c:\Users\User\cooking-agent\ai1.worktrees\copilot-worktree-2026-02-01T05-02-26\novo-projeto
```

---

### **3. Execute o script de deploy:**

```cmd
deploy_backend.bat
```

---

## 📋 O QUE VAI ACONTECER:

### **Tela 1: Verificação de Pré-requisitos**
```
[PASSO 1/8] Verificando pre-requisitos...
✓ Azure CLI instalado
✓ Git instalado
✓ Node.js instalado
```
→ **Pressione qualquer tecla**

### **Tela 2: Login no Azure**
```
[PASSO 2/8] Fazendo login no Azure...
```
→ **Navegador vai abrir**
→ **Faça login na sua conta Azure**
→ **Volte para o terminal e pressione qualquer tecla**

### **Tela 3: Resource Group**
```
[PASSO 3/8] Criando Resource Group...
✓ Resource Group criado/existente!
```
→ **Pressione qualquer tecla**

### **Tela 4: PostgreSQL (DEMORADO - 3-5 min)**
```
[PASSO 4/8] Criando PostgreSQL Server...
⏳ Isso pode levar 3-5 minutos. Aguarde...
```
→ **AGUARDE... não feche o terminal!**
→ Quando terminar, mostrará o nome do servidor
→ **Pressione qualquer tecla**

### **Tela 5: SQL Schema (AÇÃO MANUAL)**
```
[PASSO 5/8] Executar Schema SQL

⚠️ IMPORTANTE: Você precisa executar o SQL manualmente!

1. Acesse: https://portal.azure.com
2. Busque: ativo-real-db-XXXXX
3. Menu: Databases > ativo_real
4. Menu: Query editor
5. Login: adminativo / AtivO@Real2026!
6. Cole o conteúdo de: database\init\05_features_completas.sql
7. Execute
```

**FAÇA ISSO AGORA:**
1. Abra nova aba do navegador: https://portal.azure.com
2. Na barra de busca: digite o nome do servidor PostgreSQL
3. Clique no servidor
4. Menu lateral esquerdo: **Databases** → clique em `ativo_real`
5. Menu lateral esquerdo: **Query editor (preview)**
6. Faça login:
   - User: `adminativo`
   - Password: `AtivO@Real2026!`
7. Abra o arquivo: `database\init\05_features_completas.sql`
8. Copie TUDO
9. Cole no Query editor
10. Clique em **Run**

→ **Depois de executar, volte ao terminal e pressione qualquer tecla**

### **Tela 6: Function App**
```
[PASSO 6/8] Criando Function App...
```
→ **Aguarde criar Storage + Function App**
→ **Pressione qualquer tecla**

### **Tela 7: Configurações**
```
[PASSO 7/8] Configurando variáveis de ambiente...
```
→ **Aguarde configurar**
→ **Pressione qualquer tecla**

### **Tela 8: Deploy Backend (DEMORADO - 2-3 min)**
```
[PASSO 8/8] Fazendo deploy do backend...
⏳ Isso pode levar 2-3 minutos...
```
→ **AGUARDE... vai instalar dependências e fazer upload**
→ Quando ver `Deployment successful`
→ Anotará a URL do backend
→ Criará arquivo `DEPLOY_INFO.txt`

### **Tela Final: Sucesso! 🎉**
```
════════════════════════════════════════════════════════════
 ✅ DEPLOY DO BACKEND CONCLUIDO!
════════════════════════════════════════════════════════════

🔗 URL do Backend:
https://ativo-real-backend-XXXXX.azurewebsites.net/api
```

→ **ANOTE ESSA URL!**
→ **Pressione qualquer tecla**

---

## ✅ CHECKLIST DURANTE O DEPLOY:

- [ ] Comando 1: `cd` até a pasta - OK
- [ ] Comando 2: `deploy_backend.bat` - Executado
- [ ] Passo 1: Pré-requisitos verificados
- [ ] Passo 2: Login no Azure feito
- [ ] Passo 3: Resource Group criado
- [ ] Passo 4: PostgreSQL criado (~3-5 min)
- [ ] Passo 5: SQL executado no Azure Portal (MANUAL)
- [ ] Passo 6: Function App criado
- [ ] Passo 7: Variáveis configuradas
- [ ] Passo 8: Deploy backend concluído (~2-3 min)
- [ ] URL do backend anotada
- [ ] Arquivo DEPLOY_INFO.txt criado

---

## 🐛 SE DER ERRO:

### **Erro: "az: command not found"**
→ Instale Azure CLI: https://aka.ms/azure-cli
→ Reinicie o terminal após instalar

### **Erro: "Name already exists"**
→ Nome já usado no Azure
→ Execute novamente (script adiciona número aleatório)

### **Erro: PostgreSQL creation failed**
→ Tente criar manualmente no Azure Portal
→ Ou use outro nome adicionando números

### **Erro: Deploy failed**
→ Verifique logs: `az webapp log tail --name NOME-FUNCTION-APP --resource-group rg-ativo-real`
→ Ou veja logs no Azure Portal

---

## 📊 TEMPO ESTIMADO TOTAL:

- ✅ Pré-requisitos: 10 segundos
- ✅ Login: 30 segundos
- ✅ Resource Group: 10 segundos
- ⏳ PostgreSQL: **3-5 minutos**
- ✋ SQL manual: **2 minutos** (você)
- ✅ Function App: 1 minuto
- ✅ Configurações: 30 segundos
- ⏳ Deploy Backend: **2-3 minutos**

**TOTAL: ~10-12 minutos**

---

## 🎯 APÓS CONCLUIR:

Você terá:
1. ✅ **Backend no Azure** rodando em: `https://ativo-real-backend-XXXXX.azurewebsites.net/api`
2. ✅ **PostgreSQL** com 4 tabelas criadas
3. ✅ **8 endpoints** funcionando
4. ✅ **Arquivo DEPLOY_INFO.txt** com todas as credenciais

---

## 🧪 TESTAR APÓS DEPLOY:

Abra o navegador e acesse:

```
https://ativo-real-backend-XXXXX.azurewebsites.net/api/wms-layers?projeto_id=1
```

Deve retornar: `[]` (array vazio) ou lista de camadas

---

## 📝 PRÓXIMO PASSO:

Depois do backend no ar, faremos deploy do **frontend**!

---

**AGORA É SÓ EXECUTAR!** 🚀

**Abra o CMD e cole:**
```cmd
cd c:\Users\User\cooking-agent\ai1.worktrees\copilot-worktree-2026-02-01T05-02-26\novo-projeto
deploy_backend.bat
```

**BOA SORTE!** 💪
