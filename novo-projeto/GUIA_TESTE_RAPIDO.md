# 🚀 GUIA RÁPIDO DE TESTE

## Passo 1: Testar Backend

```bash
# Execute o script de teste do backend
test_backend.bat
```

Se tudo estiver OK, você verá:

```
✓ Models OK
✓ Function App OK
TUDO OK! Backend pronto para rodar
```

---

## Passo 2: Testar Frontend

```bash
# Execute o script de teste do frontend
test_frontend.bat
```

Você verá todos os componentes listados:

```
✓ ClientForm.tsx
✓ ChatWidget.tsx
✓ StatusTimeline.tsx
✓ FileUploader.tsx
✓ WMSLayerManager.tsx
✓ ContractViewer.tsx
✓ ClientPortal.tsx
```

---

## Passo 3: Iniciar os Serviços

### **Terminal 1 - Backend:**

```bash
cd backend
func start
```

Aguarde até ver:

```
Functions:
  [POST] http://localhost:7071/api/wms-layers
  [GET] http://localhost:7071/api/wms-layers
  [POST] http://localhost:7071/api/chat/messages
  [GET] http://localhost:7071/api/chat/messages
  [GET] http://localhost:7071/api/lotes/{id}/status-history
  [GET] http://localhost:7071/api/auth/magic-link/{token}
```

### **Terminal 2 - Frontend:**

```bash
cd ativo-real
npm run dev
```

Aguarde até ver:

```
  VITE v5.x.x ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## Passo 4: Testar Endpoints

### **Terminal 3 - Script de Teste:**

```bash
python test_endpoints.py
```

Você verá:

```
🚀 TESTANDO ENDPOINTS BACKEND
════════════════════════════════════════════════════════════

1️⃣ Testando WMS Layers...
   ✅ Camada criada: ID 1
   ✅ 1 camada(s) encontrada(s)
   ✅ Camada atualizada

2️⃣ Testando Chat...
   ✅ Mensagem enviada: ID 1
   ✅ 1 mensagem(ns) encontrada(s)

3️⃣ Testando Status History...
   ✅ 0 registro(s) de histórico

4️⃣ Testando Magic Link...
   ⚠️ Link inválido/expirado (esperado)

✅ TESTES CONCLUÍDOS!
```

---

## Passo 5: Testar no Browser

Abra o navegador em: **<http://localhost:5173>**

### **URLs para testar:**

1. **Homepage:**
   - `http://localhost:5173/`

2. **Dashboard (Topógrafo):**
   - `http://localhost:5173/dashboard`

3. **Portal do Cliente (precisa de token válido):**
   - `http://localhost:5173/client-portal/[token]`
   - Você pode gerar um token criando um lote no dashboard

---

## ✅ Checklist de Teste

- [ ] Backend iniciado sem erros
- [ ] Frontend iniciado sem erros
- [ ] Script de teste executado com sucesso
- [ ] Todos os 8 endpoints respondendo
- [ ] Homepage carregando
- [ ] Dashboard acessível
- [ ] Componentes renderizando corretamente

---

## 🐛 Troubleshooting

### **Erro: "Module not found"**

```bash
cd backend
pip install -r requirements.txt
pip install azure-functions geoalchemy2
```

### **Erro: "Database connection failed"**

- Verifique se o PostgreSQL está rodando
- Verifique a `DATABASE_URL` no `.env`

### **Erro: Frontend não compila**

```bash
cd ativo-real
rm -rf node_modules package-lock.json
npm install
```

### **Erro: "Port already in use"**

- Backend: Mude a porta no `local.settings.json`
- Frontend: Use `npm run dev -- --port 5174`

---

## 🎯 Próximos Passos Após Testes

1. **Se tudo funcionar localmente:**
   - Commit das alterações
   - Push para GitHub
   - Deploy no Azure

2. **Se houver erros:**
   - Verifique os logs
   - Consulte os arquivos de documentação:
     - `SOLUCOES_IMPLEMENTADAS.md`
     - `FRONTEND_IMPLEMENTADO.md`
     - `IMPLEMENTACAO_FINAL_COMPLETA.md`

---

**Pronto para testar!** Execute `test_backend.bat` e `test_frontend.bat` 🚀
