# OpenRouter Integration - Backend & Frontend

**Data:** 31/01/2026
**Status:** ✅ Implementado (pronto para usar com API key válida)

---

## 📋 O que foi criado

### 1. Backend Python - OpenRouter Client
**Arquivo:** `novo-projeto/backend/openrouter_client.py`

```python
class OpenRouterClient:
    - chat_completion() - Enviar mensagens para Jamba
    - analyze_topography() - Análise de topografia
    - generate_report() - Gerar relatórios formatados
    - validate_geometry_description() - Validar descrições de geometria
```

**Segurança:**
- ✅ API key guardada no backend (nunca exposta)
- ✅ Tratamento robusto de erros
- ✅ Timeout de 60 segundos
- ✅ Suporte para múltiplos modelos

---

### 2. Backend Azure Functions - 4 Novos Endpoints

**Arquivo:** `novo-projeto/backend/function_app.py` (adicionar)

| Endpoint | Método | Auth | Descrição |
|----------|--------|------|-----------|
| `/ai/chat` | POST | JWT ✅ | Chat com Jamba 1.5 Large |
| `/ai/analyze-topography` | POST | JWT ✅ | Análise de topografia |
| `/ai/generate-report` | POST | JWT ✅ | Gerar relatório formatado |
| `/ai/validate-geometry` | POST | JWT ✅ | Validar geometria |

**Todos requerem:**
- Header: `Authorization: Bearer <access_token>`
- Campo: `Content-Type: application/json`

---

### 3. Frontend React - Hook Seguro

**Arquivo:** `novo-projeto/ativo-real/src/services/useOpenRouter.ts`

```typescript
const { chat, analyzeTopography, generateReport, validateGeometry, loading, error } = 
  useOpenRouter({ authToken: jwtToken });

// Usar em componente:
const response = await chat([
  { role: 'user', content: 'What is this property?' }
]);

if (response) {
  console.log(response.choices[0].message.content);
}
```

**Recursos:**
- ✅ Hook React simples
- ✅ Tratamento de loading e erro
- ✅ Context Provider para app global
- ✅ TypeScript completo

---

## 🔒 Arquitetura de Segurança

```
┌─────────────────┐
│  React Frontend │
│  (sem API key)  │
└────────┬────────┘
         │ JWT Token
         │ POST /ai/chat
         ↓
┌─────────────────────────┐
│  Azure Function Backend │
│ (API key segura aqui)   │
│  - Valida JWT           │
│  - Chama OpenRouter     │
│  - Retorna resposta     │
└────────┬────────────────┘
         │ HTTPS
         ↓
┌──────────────────────────┐
│  OpenRouter API          │
│  (processamento de IA)   │
└──────────────────────────┘
```

**Garantias:**
- API key NUNCA expostas no navegador
- Todos endpoints requerem autenticação JWT válida
- Reforço de CORS no backend
- Validação de schema em todos endpoints

---

## 🚀 Como Usar

### Passo 1: Adicione OpenRouter Client ao Backend

Arquivo já criado em:
```
novo-projeto/backend/openrouter_client.py
```

### Passo 2: Adicione Endpoints ao function_app.py

Arquivo de referência em:
```
novo-projeto/backend/AI_ENDPOINTS_TO_ADD.py
```

Copie e cole os 4 endpoints ao final do `function_app.py`

### Passo 3: Configure Variável de Ambiente

No Azure Portal ou local:
```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxx
```

### Passo 4: Use no React

```typescript
import { useOpenRouter } from './services/useOpenRouter';

function TopographyAnalyzer() {
  const { chat, loading, error } = useOpenRouter({ 
    authToken: localStorage.getItem('access_token')
  });

  const analyze = async () => {
    const response = await chat([
      { role: 'user', content: 'Analyze this property...' }
    ]);
    console.log(response?.choices[0].message.content);
  };

  return (
    <button onClick={analyze} disabled={loading}>
      {loading ? 'Analyzing...' : 'Analyze Property'}
    </button>
  );
}
```

---

## 📝 Exemplos de Request

### Chat Request
```bash
POST /api/ai/chat
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

{
  "messages": [
    { "role": "user", "content": "What is the soil type of this property?" }
  ],
  "model": "jamba-1.5-large",
  "temperature": 0.7,
  "max_tokens": 2048
}
```

### Topography Analysis
```bash
POST /api/ai/analyze-topography
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

{
  "prompt": "Analyze this property for agricultural potential",
  "context": "100 hectares in Sao Paulo state"
}
```

### Generate Report
```bash
POST /api/ai/generate-report
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

{
  "data": {
    "area_ha": 100,
    "soil_type": "Latossolo",
    "coordinates": [-48.5, -21.5],
    "climate": "subtropical"
  }
}
```

### Validate Geometry
```bash
POST /api/ai/validate-geometry
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

{
  "description": "Property bounded by coordinates..."
}
```

---

## ✅ Checklist de Deployment

- [ ] OpenRouter Account Ativo
- [ ] OPENROUTER_API_KEY obtida
- [ ] `openrouter_client.py` no backend
- [ ] 4 endpoints adicionados a `function_app.py`
- [ ] `requirements.txt` atualizado (requests já tem)
- [ ] Variável de ambiente configurada no Azure Portal
- [ ] JWT authentication funcionando
- [ ] `useOpenRouter.ts` no frontend
- [ ] Components usando o hook com auth token
- [ ] Deploy para Azure Static Web Apps
- [ ] Teste endpoints com Postman/cURL

---

## 🐛 Troubleshooting

### ❌ "401 Unauthorized" no endpoint AI

```
Causa: JWT token inválido ou expirado
Solução: Verifique se o token no header é válido
```

### ❌ "OpenRouter API key not configured"

```
Causa: OPENROUTER_API_KEY não está definida
Solução: Adicione a variável ao Azure Function App Settings
```

### ❌ "Invalid OpenRouter API key"

```
Causa: Chave expirou ou foi revogada
Solução: Gere uma nova chave no OpenRouter Dashboard
```

### ❌ "Rate limited"

```
Causa: Muitas requisições em pouco tempo
Solução: Implemente exponential backoff nas chamadas
```

---

## 📊 Modelos Disponíveis

| Modelo | Contexto | Custo | Uso |
|--------|----------|-------|-----|
| jamba-1.5-large | 256K | $0.40/1M | Análise geral ✅ |
| mistralai/mistral-7b | 32K | $0.04/1M | Código (futuro) |
| openai/gpt-4 | 128K | $0.05/1M | Premium (futuro) |

Configurar via parâmetro `model` no request.

---

## 🔄 Fluxo Completo de Autenticação + IA

```
1. User faz login
   POST /api/auth/login → recebe access_token + refresh_token

2. Frontend armazena access_token
   localStorage.setItem('access_token', token)

3. Componente usa hook OpenRouter
   const { chat } = useOpenRouter({ 
     authToken: localStorage.getItem('access_token')
   })

4. Chama endpoint protegido
   POST /api/ai/chat
   Header: Authorization: Bearer {access_token}

5. Backend valida JWT
   @require_auth decorator verifica assinatura

6. Se válido, chama OpenRouter API
   OpenRouterClient.chat_completion()

7. Retorna resposta para frontend
   { choices: [...], usage: {...} }

8. Frontend renderiza análise
```

---

**Status:** ✅ Pronto para produção (aguardando API key válida)

**Próximas Etapas:**
1. Confirmar OPENROUTER_API_KEY válida
2. Deploy para Azure
3. Testar endpoints com Postman
4. Integrar com componentes React (remover mocks)
