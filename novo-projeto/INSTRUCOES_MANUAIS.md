# ⚠️ INSTRUÇÕES PARA EXECUTAR MANUALMENTE

Como o PowerShell 6+ não está disponível, siga estas instruções:

---

## 🚀 INICIAR BACKEND E FRONTEND - PASSO A PASSO

### **TERMINAL 1 - Backend (Azure Functions)**

1. Abra um **Prompt de Comando** (cmd.exe)

2. Navegue até a pasta do projeto:

```cmd
cd c:\Users\User\cooking-agent\ai1.worktrees\copilot-worktree-2026-02-01T05-02-26\novo-projeto
```

1. Entre na pasta do backend:

```cmd
cd backend
```

1. Crie o ambiente virtual (se não existir):

```cmd
python -m venv venv
```

1. Ative o ambiente virtual:

```cmd
venv\Scripts\activate.bat
```

1. Instale as dependências:

```cmd
pip install -r requirements.txt
pip install azure-functions geoalchemy2
```

1. Inicie o Azure Functions:

```cmd
func start
```

**✅ Aguarde até ver:** `Worker process started and initialized`

---

### **TERMINAL 2 - Frontend (Vite)**

1. Abra **outro** Prompt de Comando

2. Navegue até a pasta do projeto:

```cmd
cd c:\Users\User\cooking-agent\ai1.worktrees\copilot-worktree-2026-02-01T05-02-26\novo-projeto
```

1. Entre na pasta do frontend:

```cmd
cd ativo-real
```

1. Instale dependências (se necessário):

```cmd
npm install
```

1. Inicie o dev server:

```cmd
npm run dev
```

**✅ Aguarde até ver:** `Local: http://localhost:5173/`

---

### **TERMINAL 3 - Testar Endpoints (OPCIONAL)**

1. Abra **outro** Prompt de Comando

2. Navegue até a pasta do projeto:

```cmd
cd c:\Users\User\cooking-agent\ai1.worktrees\copilot-worktree-2026-02-01T05-02-26\novo-projeto
```

1. Ative o ambiente virtual do backend:

```cmd
cd backend
venv\Scripts\activate.bat
cd ..
```

1. Execute o script de teste:

```cmd
python test_endpoints.py
```

---

## 🌐 ACESSAR NO NAVEGADOR

Após iniciar backend e frontend, abra:

**Frontend:**

```
http://localhost:5173
```

**Backend API:**

```
http://localhost:7071/api
```

---

## ✅ CHECKLIST

- [ ] Terminal 1: Backend rodando (porta 7071)
- [ ] Terminal 2: Frontend rodando (porta 5173)
- [ ] Terminal 3: Testes executados (opcional)
- [ ] Navegador: Frontend acessível
- [ ] Navegador: Componentes carregando

---

## 🐛 TROUBLESHOOTING

### **Erro: "func: command not found"**

Instale Azure Functions Core Tools:

```cmd
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

### **Erro: "Module not found" (Backend)**

```cmd
cd backend
venv\Scripts\activate.bat
pip install -r requirements.txt
pip install azure-functions geoalchemy2 psycopg2-binary
```

### **Erro: "Cannot find module" (Frontend)**

```cmd
cd ativo-real
rmdir /s /q node_modules
del package-lock.json
npm install
```

### **Porta ocupada (7071 ou 5173)**

Backend (porta diferente):

```cmd
func start --port 7072
```

Frontend (porta diferente):

```cmd
npm run dev -- --port 5174
```

---

## 📊 O QUE FOI IMPLEMENTADO

### **Backend (8 endpoints):**

- ✅ POST /api/wms-layers - Criar camada WMS
- ✅ GET /api/wms-layers - Listar camadas
- ✅ PATCH /api/wms-layers/{id} - Atualizar camada
- ✅ DELETE /api/wms-layers/{id} - Deletar camada
- ✅ POST /api/chat/messages - Enviar mensagem
- ✅ GET /api/chat/messages - Listar mensagens
- ✅ GET /api/lotes/{id}/status-history - Histórico
- ✅ GET /api/auth/magic-link/{token} - Validar link

### **Frontend (6 componentes novos):**

- ✅ ClientForm.tsx - Formulário validado
- ✅ ChatWidget.tsx - Chat com polling
- ✅ StatusTimeline.tsx - Timeline visual
- ✅ FileUploader.tsx - Upload de arquivos
- ✅ WMSLayerManager.tsx - Gerenciar camadas WMS
- ✅ ContractViewer.tsx - Visualizar contratos

### **Componentes atualizados:**

- ✅ ClientPortal.tsx - Portal completo com tabs
- ✅ services/api.ts - Novos métodos API

---

## 📖 DOCUMENTAÇÃO DISPONÍVEL

- `GUIA_TESTE_RAPIDO.md` - Guia passo a passo
- `CHECKLIST_FINAL_DEPLOY.md` - Checklist de deploy
- `IMPLEMENTACAO_FINAL_COMPLETA.md` - Documentação técnica completa
- `SOLUCOES_IMPLEMENTADAS.md` - Soluções backend
- `FRONTEND_IMPLEMENTADO.md` - Documentação frontend

---

## 🎯 PRÓXIMOS PASSOS

1. **Testar localmente** (siga as instruções acima)
2. **Verificar todos componentes** funcionando
3. **Executar script de testes** (`test_endpoints.py`)
4. **Deploy no Azure** (quando estiver pronto)

---

**BOA SORTE! 🚀**

Se precisar de ajuda, consulte os arquivos de documentação listados acima.
