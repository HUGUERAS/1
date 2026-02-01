# 🚀 OpenRouter Integration - Quick Start

## Por que OpenRouter?

✅ **Uma API key** para 200+ modelos  
✅ **Mais barato** que APIs diretas  
✅ **Streaming nativo**  
✅ **Fallback automático** entre providers  
✅ **Analytics integrado**  

### Comparação de Preços (1M tokens)

| Provider | Jamba 1.7 Large | GPT-4 Turbo |
|----------|-----------------|-------------|
| **OpenRouter** | **$0.40** | $8.00 |
| AI21 Direto | $0.50 | N/A |
| OpenAI Direto | N/A | $10.00 |

**OpenRouter é 20% mais barato!** 💰

---

## 🔧 Setup em 3 passos

### 1. Obter API Key (Grátis)

```bash
# Criar conta em:
https://openrouter.ai/

# Ir para Keys → Create Key
# Copiar a key
```

### 2. Instalar SDK

```bash
pip install openrouter-sdk
```

### 3. Configurar

```bash
# Azure Functions: local.settings.json
{
  "Values": {
    "OPENROUTER_API_KEY": "sk-or-v1-xxxxx"
  }
}

# Ou variável de ambiente
export OPENROUTER_API_KEY="sk-or-v1-xxxxx"
```

---

## 💻 Uso Básico

### Exemplo 1: Análise Simples

```python
from jamba_openrouter import JambaStructureAnalyzer, AIProvider

analyzer = JambaStructureAnalyzer(
    provider=AIProvider.OPENROUTER,
    model="large"  # jamba-large-1.7
)

# Analisar arquitetura
files = [
    {"path": "backend/models.py", "content": "...código..."},
    {"path": "frontend/App.tsx", "content": "...código..."}
]

result = await analyzer.analyze_project_structure(
    files,
    analysis_type="architecture",
    stream=False
)

print(result["content"])
```

### Exemplo 2: Streaming em Tempo Real

```python
# Análise com streaming (melhor UX)
stream = await analyzer.analyze_project_structure(
    files,
    analysis_type="refactor",
    stream=True  # 🌊 Retorna tokens conforme gerados
)

# Imprimir tokens em tempo real
async for chunk in stream:
    print(chunk, end="", flush=True)
```

### Exemplo 3: Code Review de PR

```python
git_diff = """
diff --git a/backend/auth.py b/backend/auth.py
+def require_auth(func):
+    @wraps(func)
+    def wrapper(req):
+        # autenticação
"""

review = await analyzer.code_review(
    diff=git_diff,
    context="Feature: JWT Authentication",
    stream=False
)

print(review["content"])
```

---

## 🎨 Frontend Integration

### React Component com Streaming

```typescript
// frontend/src/components/AIAnalyzer.tsx
import { useState } from 'react';

export const AIAnalyzer = () => {
  const [analysis, setAnalysis] = useState('');
  const [streaming, setStreaming] = useState(false);

  const analyzeProject = async () => {
    setStreaming(true);
    setAnalysis('');

    const response = await fetch('/api/ai/analyze-streaming', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        files: projectFiles,
        analysis_type: 'architecture'
      })
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader!.read();
      if (done) break;

      const chunk = decoder.decode(value);
      setAnalysis(prev => prev + chunk);
    }

    setStreaming(false);
  };

  return (
    <div>
      <button onClick={analyzeProject} disabled={streaming}>
        {streaming ? '🧠 Analisando...' : '🔍 Analisar Projeto'}
      </button>
      
      {streaming && <div className="loading-indicator">⏳</div>}
      
      <pre className="analysis-output">
        {analysis}
        {streaming && <span className="cursor">▊</span>}
      </pre>
    </div>
  );
};
```

---

## 🔌 Endpoint Azure Functions

```python
# backend/function_app.py
import azure.functions as func
from jamba_openrouter import JambaStructureAnalyzer, AIProvider

@app.route(route="ai/analyze-streaming", methods=["POST"])
@require_auth
async def analyze_streaming(req: func.HttpRequest) -> func.HttpResponse:
    """Análise com streaming via Server-Sent Events"""
    
    try:
        body = req.get_json()
        files = body.get("files", [])
        analysis_type = body.get("analysis_type", "architecture")
        
        analyzer = JambaStructureAnalyzer(
            provider=AIProvider.OPENROUTER,
            model="large"
        )
        
        # Streaming response
        async def generate():
            stream = await analyzer.analyze_project_structure(
                files, 
                analysis_type, 
                stream=True
            )
            
            async for chunk in stream:
                yield f"data: {chunk}\n\n"
        
        return func.HttpResponse(
            generate(),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
```

---

## 🎯 Modelos Disponíveis via OpenRouter

### Jamba Family

```python
JAMBA_MODELS = {
    "large": "ai21/jamba-large-1.7",      # 256K, melhor qualidade
    "mini": "ai21/jamba-mini-1.5",        # 256K, mais rápido/barato
    "instruct": "ai21/jamba-1.5-instruct" # Fine-tuned para comandos
}
```

### Outros Modelos (Fallback)

```python
# Se Jamba estiver indisponível
FALLBACK_MODELS = {
    "gpt4": "openai/gpt-4-turbo",
    "claude": "anthropic/claude-3-opus",
    "mixtral": "mistralai/mixtral-8x22b-instruct"
}
```

---

## 📊 Analytics Dashboard

OpenRouter oferece analytics gratuito:

```
https://openrouter.ai/activity

- Tokens usados
- Custo total
- Latência por modelo
- Taxa de erro
- Uso por endpoint
```

---

## 🔒 Segurança

### Variáveis de Ambiente

```bash
# ✅ CORRETO
export OPENROUTER_API_KEY="sk-or-v1-xxxxx"

# ❌ ERRADO - nunca commitar
API_KEY = "sk-or-v1-xxxxx"
```

### Azure Key Vault (Produção)

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(
    vault_url="https://ativoreal-vault.vault.azure.net/",
    credential=credential
)

OPENROUTER_API_KEY = client.get_secret("OPENROUTER-API-KEY").value
```

---

## 🧪 Testes

```python
# tests/test_jamba_openrouter.py
import pytest
from jamba_openrouter import JambaStructureAnalyzer, AIProvider

@pytest.mark.asyncio
async def test_analyze_architecture():
    analyzer = JambaStructureAnalyzer(
        provider=AIProvider.MOCK  # Usar MOCK em testes
    )
    
    files = [{"path": "test.py", "content": "print('hello')"}]
    result = await analyzer.analyze_project_structure(files, "architecture")
    
    assert result["success"] == True
    assert "content" in result

@pytest.mark.asyncio
async def test_streaming():
    analyzer = JambaStructureAnalyzer(provider=AIProvider.MOCK)
    
    stream = await analyzer.analyze_project_structure([], "refactor", stream=True)
    
    chunks = []
    async for chunk in stream:
        chunks.append(chunk)
    
    assert len(chunks) > 0
```

---

## 🆘 Troubleshooting

### Erro: "OPENROUTER_API_KEY not set"

```bash
# Verificar
echo $OPENROUTER_API_KEY

# Configurar
export OPENROUTER_API_KEY="sk-or-v1-xxxxx"
```

### Erro: "Rate limit exceeded"

```python
# Adicionar retry com backoff
import asyncio

async def analyze_with_retry(analyzer, files):
    for attempt in range(3):
        try:
            return await analyzer.analyze_project_structure(files)
        except Exception as e:
            if "rate limit" in str(e).lower():
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
```

### Modo Mock para Desenvolvimento

```python
# Desenvolver sem gastar tokens
analyzer = JambaStructureAnalyzer(provider=AIProvider.MOCK)

# Retorna respostas simuladas
result = await analyzer.analyze_project_structure([...])
```

---

## 📖 Referências

- [OpenRouter Docs](https://openrouter.ai/docs)
- [OpenRouter SDK](https://github.com/OpenRouterTeam/openrouter-python)
- [Jamba Model Card](https://www.ai21.com/jamba)
- [Pricing](https://openrouter.ai/models/ai21/jamba-large-1.7)

---

## 🚀 Quick Commands

```bash
# Instalar
pip install openrouter-sdk

# Configurar
export OPENROUTER_API_KEY="sk-or-v1-xxxxx"

# Testar
python backend/jamba_openrouter.py

# Deploy Azure
az functionapp config appsettings set \
  --name func-ativoreal \
  --resource-group ativoreal-rg \
  --settings OPENROUTER_API_KEY="sk-or-v1-xxxxx"
```

**Pronto para produção!** ✅
