# OpenRouter API - Teste e Validação

## Status Atual

✅ **InfinitePay isolado** - Desabilitado temporariamente do `function_app.py`
- Import comentado: `# from infinitepay_payment import infinitepay_bp`
- Blueprint registration comentado: `# app.register_functions(infinitepay_bp)`
- O backend agora funciona sem InfinitePay até que a chave seja configurada

⏳ **OpenRouter** - Pronto para teste com sua API key

## Pré-requisitos

Você precisa ter:
1. **OPENROUTER_API_KEY** - A chave que você recebeu do OpenRouter
2. **Python 3.11+** - Para rodar o script de teste
3. **PowerShell** - Para rodar o script .ps1 (Windows)
4. **Conexão com internet** - Para alcançar `https://openrouter.ai/`

## Como Testar

### Opção 1: PowerShell (Recomendado para Windows)

```powershell
# 1. Defina a variável de ambiente com sua chave
$env:OPENROUTER_API_KEY = "sk-or-v1-xxxxxxxxxxxxx"

# 2. Execute o script de teste
cd c:\Users\User\cooking-agent\ai1\novo-projeto
.\test_openrouter.ps1

# (Opcional) Para mais detalhes, use -Verbose
.\test_openrouter.ps1 -Verbose
```

**Saída esperada:**
```
✓ API key found (45 characters)
✓ OpenRouter API responded successfully (HTTP 200)
Model Response: Funcionando perfeitamente!...
✓ Valid response structure from Jamba 1.5 Large
```

### Opção 2: Python

```bash
# 1. Defina a variável de ambiente com sua chave
export OPENROUTER_API_KEY="sk-or-v1-xxxxxxxxxxxxx"  # Linux/Mac
set OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx      # Windows CMD

# 2. Execute o script de teste
cd c:\Users\User\cooking-agent\ai1\novo-projeto
python test_openrouter.py
```

**Saída esperada:**
```
✓ API key found (45 characters)
✓ OpenRouter API responded successfully (HTTP 200)
Model Response: Funcionando perfeitamente!...
✓ Valid response structure from Jamba 1.5 Large
```

## Modelo Testado

| Aspecto | Valor |
|---------|-------|
| **Modelo Primário** | `jamba-1.5-large` |
| **Contexto** | 256K tokens |
| **Custo** | $0.40/1M tokens (input) |
| **Latência** | ~1-2 segundos |
| **Caso de Uso** | Análise de topografia, geração de relatórios, processamento de geometrias |

## Próximas Etapas

Após validar que OpenRouter funciona, vamos:

1. ✅ Remover `AIProvider.MOCK` do `jamba_openrouter.py`
2. ✅ Remover mocks de `jamba_analyzer.py`
3. ✅ Integrar OpenRouter no backend (endpoints que usam IA)
4. ✅ Testar endpoints protegidos com JWT
5. ✅ Remover mocks do frontend (DashboardTopografo.tsx, GlobalMapValidacao.tsx)

## Troubleshooting

### ✗ "OPENROUTER_API_KEY not found"
- **Causa:** Variável de ambiente não foi definida
- **Solução:** Execute um dos comandos de definição acima antes do teste

### ✗ "Authentication failed (HTTP 401)"
- **Causa:** API key inválida ou expirada
- **Solução:** Verifique se você copiou corretamente a chave do OpenRouter dashboard

### ✗ "Connection error - OpenRouter API unreachable"
- **Causa:** Sem conexão com internet ou firewall bloqueando openrouter.ai
- **Solução:** Verifique sua conexão de internet

### ⚠ "Rate limited (HTTP 429)"
- **Causa:** Muitas requisições em pouco tempo
- **Solução:** Aguarde alguns minutos antes de tentar novamente

## Documentação de Referência

- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [Jamba Model Card](https://huggingface.co/ai21labs/Jamba-v0.1)
- [Pricing & Models](https://openrouter.ai/models)

## Chave de Ambiente Para Desenvolvimento

Caso precise adicionar permanentemente ao seu ambiente:

### PowerShell (Persistente)
```powershell
# Editar variáveis de ambiente do sistema
[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-v1-xxxxxxxxxxxxx", "User")

# Fechar e reabrir PowerShell para que a mudança tenha efeito
```

### Windows CMD (Persistente)
```batch
setx OPENROUTER_API_KEY "sk-or-v1-xxxxxxxxxxxxx"
```

### .env File (Local - Não fazer commit)
```
# novo-projeto/.env (ignored by .gitignore)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
OPENROUTER_API_KEY_FALLBACK=sk-or-v1-yyyyyyyyyyyyyyy
```

---

**Status:** ✅ Pronto para teste
**Data:** 31/01/2026
**Próxima Ação:** Execute um dos scripts de teste acima e confirme sucesso
