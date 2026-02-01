# Quick Start - OpenRouter Integration

## ✅ O que foi feito:

### Backend (Python)
1. ✅ `openrouter_client.py` - Cliente OpenRouter
2. ✅ `function_app.py` - 4 endpoints AI adicionados:
   - `POST /ai/chat`
   - `POST /ai/analyze-topography`
   - `POST /ai/generate-report`
   - `POST /ai/validate-geometry`

### Frontend (React/TypeScript)
1. ✅ `src/services/useOpenRouter.ts` - Hook React
2. ✅ `src/components/AIAssistant.tsx` - Componente de exemplo

### Testes
1. ✅ `backend/test_ai_endpoints.ps1` - Script de teste PowerShell

---

## 🚀 Como testar localmente:

### 1. Configure OPENROUTER_API_KEY

```powershell
# No terminal PowerShell:
$env:OPENROUTER_API_KEY = "sua-chave-valida-aqui"
```

### 2. Inicie o Backend

```powershell
cd c:\Users\User\cooking-agent\ai1\novo-projeto\backend
func start
```

### 3. Faça Login (obtenha JWT token)

```powershell
$loginResponse = Invoke-RestMethod -Uri "http://localhost:7071/api/auth/login" -Method Post -Body (@{
    email = "admin@ativoreal.com"
    password = "Admin123!"
} | ConvertTo-Json) -ContentType "application/json"

$token = $loginResponse.access_token
Write-Host "Token: $token"
```

### 4. Teste os Endpoints AI

```powershell
.\test_ai_endpoints.ps1 -AccessToken $token
```

**Ou manualmente:**

```powershell
# Chat com AI
$chatResponse = Invoke-RestMethod -Uri "http://localhost:7071/api/ai/chat" -Method Post `
  -Headers @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
  } `
  -Body (@{
    messages = @(
      @{ role = "user"; content = "What is the best soil for coffee?" }
    )
  } | ConvertTo-Json)

Write-Host $chatResponse.choices[0].message.content
```

---

## 🎨 Como usar no Frontend React:

### Opção 1: Hook direto no componente

```typescript
import { useOpenRouter } from './services/useOpenRouter';

function MyComponent() {
  const accessToken = localStorage.getItem('access_token');
  const { chat, loading, error } = useOpenRouter({ authToken: accessToken });

  const handleChat = async () => {
    const response = await chat([
      { role: 'user', content: 'Analyze this property...' }
    ]);
    
    if (response) {
      console.log(response.choices[0].message.content);
    }
  };

  return (
    <button onClick={handleChat} disabled={loading}>
      {loading ? 'Analyzing...' : 'Analyze'}
    </button>
  );
}
```

### Opção 2: Componente completo (AIAssistant.tsx)

```typescript
import AIAssistant from './components/AIAssistant';

function App() {
  return <AIAssistant />;
}
```

---

## 📦 Deploy para Azure:

### 1. Adicione variável de ambiente no Azure Portal

```
Azure Portal → Function App → Settings → Configuration → New application setting

Name: OPENROUTER_API_KEY
Value: sk-or-v1-xxxxxxxxxxxx
```

### 2. Deploy backend

```powershell
cd novo-projeto/backend
func azure functionapp publish <seu-function-app-name>
```

### 3. Atualize frontend .env

```bash
# novo-projeto/ativo-real/.env.production
REACT_APP_API_URL=https://<seu-function-app>.azurewebsites.net/api
```

### 4. Deploy frontend

```powershell
cd novo-projeto/ativo-real
npm run build
swa deploy
```

---

## 🔑 Onde conseguir OPENROUTER_API_KEY válida:

1. Acesse: https://openrouter.ai/
2. Faça login/cadastro
3. Vá para: Settings → API Keys
4. Clique em "Create Key"
5. Copie a chave (começa com `sk-or-v1-...`)
6. Use nos testes acima

**Nota:** A chave testada anteriormente (`sk-or-v1-2738bdc...`) retornou "User not found", então você precisa gerar uma nova.

---

## ✅ Checklist:

- [x] Backend: openrouter_client.py criado
- [x] Backend: 4 endpoints AI adicionados
- [x] Frontend: useOpenRouter hook criado
- [x] Frontend: AIAssistant componente exemplo
- [x] Testes: script PowerShell criado
- [ ] **Obter OPENROUTER_API_KEY válida** ← Você precisa fazer
- [ ] Testar localmente com func start
- [ ] Deploy para Azure

---

**Status:** ✅ Código pronto, aguardando API key válida para testes
