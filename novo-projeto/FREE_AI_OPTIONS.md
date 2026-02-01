# Opções de AI GRATUITAS para Backend

## 🆓 OPÇÃO 1: GitHub Models (GRÁTIS com GitHub Copilot)

**Endpoint:** `https://models.inference.ai.azure.com`

**Modelos gratuitos disponíveis:**
- `gpt-4o` (128K context) - Melhor qualidade
- `gpt-4o-mini` (128K context) - Mais rápido
- `Phi-3.5-mini` (128K context) - Pequeno e eficiente
- `Mistral-large-2` (128K context) - Bom para análise técnica
- `Llama-3.1-70B` (128K context) - Open source

**Como usar:**
1. Obter token em: https://github.com/settings/tokens
2. Criar token com scope `user:email`
3. Configurar: `GITHUB_TOKEN=ghp_xxx`

**Código:**
```python
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

response = requests.post(
    "https://models.inference.ai.azure.com/chat/completions",
    headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    },
    json={
        "model": "gpt-4o",  # ou "Mistral-large-2"
        "messages": [{"role": "user", "content": "Analise este projeto..."}],
        "max_tokens": 4096
    }
)
```

**Vantagens:**
- ✅ **100% GRÁTIS** (limite de rate, mas generoso)
- ✅ **GPT-4o incluído** (modelo top tier)
- ✅ **Já tem Copilot** = já paga = pode usar
- ✅ **Sem custo por token**

---

## 💰 OPÇÃO 2: OpenRouter (Pay-per-use)

**Modelos recomendados:**

### Mais Barato:
- `google/gemini-2.0-flash-lite-001`: $0.07 / $0.30 por 1M tokens
- `minimax/minimax-01`: $0.20 / $1.10 por 1M tokens (1M context!)

### Melhor Qualidade:
- `ai21/jamba-large-1.7`: $2.00 / $8.00 por 1M tokens (atual)
- `anthropic/claude-3.5-sonnet`: $6.00 / $30.00 por 1M tokens

### Ultra-Barato (Experimentos):
- `x-ai/grok-4.1-fast`: $0.20 / $0.50 por 1M tokens (2M context!)

**Custo estimado mensal:**
- 10K requests x 1K tokens avg = 10M tokens = $0.70-$2.00/mês (gemini)
- Muito mais barato que $10-20/mês de outro serviço

---

## 🎯 RECOMENDAÇÃO FINAL

### Para Desenvolvimento/Testes:
**Use GitHub Models (GRÁTIS)** ✅
- Já tem Copilot? Use GPT-4o grátis!
- Limite de rate: ~15 requests/min (suficiente para dev)

### Para Produção:
**OpenRouter com Gemini Flash** ($0.07/1M tokens) 💰
- Contexto 1M tokens (4x maior que GPT-4o)
- Custo ridiculamente baixo
- Sem rate limits agressivos

---

## 📝 Como Migrar para GitHub Models (GRÁTIS)

1. **Obter Token:**
   ```powershell
   # Abrir: https://github.com/settings/tokens
   # Criar token com scope: user:email
   ```

2. **Configurar Backend:**
   ```python
   # openrouter_client.py
   GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
   
   if GITHUB_TOKEN:
       endpoint = "https://models.inference.ai.azure.com"
       model = "gpt-4o"  # GRÁTIS!
   elif OPENROUTER_API_KEY:
       endpoint = "https://openrouter.ai/api/v1"
       model = "google/gemini-2.0-flash-lite-001"  # $0.07
   ```

3. **Testar:**
   ```powershell
   $env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxxx"
   python test_github_models.py
   ```

---

## 💡 Resumo Rápido

| Opção | Custo | Context | Qualidade | Rate Limit |
|-------|-------|---------|-----------|------------|
| **GitHub Models GPT-4o** | 🆓 GRÁTIS | 128K | ⭐⭐⭐⭐⭐ | ~15 req/min |
| **OpenRouter Gemini Lite** | $0.07/1M | 1M | ⭐⭐⭐⭐ | Sem limite |
| **OpenRouter Jamba** (atual) | $2.00/1M | 256K | ⭐⭐⭐⭐ | Sem limite |
| **OpenRouter Claude** | $6.00/1M | 200K | ⭐⭐⭐⭐⭐ | Sem limite |

**Melhor estratégia:**
1. Dev/Testes: **GitHub Models** (grátis)
2. Produção: **OpenRouter Gemini** ($0.07 = quase grátis)
3. Análises críticas: **OpenRouter Claude** (premium)
