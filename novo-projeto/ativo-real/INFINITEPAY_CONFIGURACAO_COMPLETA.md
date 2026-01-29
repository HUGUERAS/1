# ✅ Configuração InfinitePay - COMPLETA

## 🎉 O Que Foi Feito Automaticamente

### 1. **Azure Function App Criada**
- Nome: `func-ativoreal-api`
- URL: https://func-ativoreal-api.azurewebsites.net
- Runtime: Python 3.11
- Plan: Consumption (paga por execução)
- Storage: `staativoreal7325`

### 2. **Endpoints Publicados** ✅
```
✅ POST /api/infinitepay/create-payment
✅ POST /api/infinitepay/webhook
✅ GET  /api/infinitepay/check-status/{payment_id}
✅ POST /api/rural/onboard
✅ POST /api/tech/login
✅ POST /api/urban/activate
✅ POST /api/login
✅ GET  /api/rural/dashboard/{user_id}
```

### 3. **Variáveis de Ambiente Configuradas** ✅
```env
INFINITEPAY_API_KEY=sk_test_COLOQUE_SUA_CHAVE_AQUI
FRONTEND_URL=https://gray-plant-08ef6cf0f.2.azurestaticapps.net
FUNCTION_APP_URL=https://func-ativoreal-api.azurewebsites.net
```

### 4. **CORS Habilitado** ✅
- Frontend: `https://gray-plant-08ef6cf0f.2.azurestaticapps.net`
- Localhost: `http://localhost:5173`

### 5. **Frontend Atualizado e Deployado** ✅
- Variável `VITE_API_BASE` configurada
- Build: 759.33 KB (226.91 KB gzipped)
- Deploy: https://gray-plant-08ef6cf0f.2.azurestaticapps.net

---

## ⚠️ O Que VOCÊ Precisa Fazer Agora

### **1. Obter API Key do InfinitePay (SANDBOX)**

1. Criar conta: https://dashboard.infinitepay.io/signup
2. Verificar email
3. Acessar: **Dashboard → Configurações → API Keys**
4. Copiar chave **Sandbox** (começa com `sk_test_`)

### **2. Atualizar API Key no Azure**

**Opção A - Portal Azure** (mais fácil):
1. Acesse: https://portal.azure.com
2. Busque: `func-ativoreal-api`
3. Vá em: **Configuration** → **Application settings**
4. Edite `INFINITEPAY_API_KEY`
5. Cole sua chave sandbox: `sk_test_xxxxxxxxxxxxx`
6. Click **Save** → **Continue**

**Opção B - Linha de comando**:
```powershell
az functionapp config appsettings set `
  --name func-ativoreal-api `
  --resource-group rg-ativoreal-chile `
  --settings INFINITEPAY_API_KEY="sk_test_SUA_CHAVE_AQUI"
```

### **3. Configurar Webhook no InfinitePay**

1. Dashboard InfinitePay → **Webhooks** → **+ Novo**
2. **URL do Webhook**:
   ```
   https://func-ativoreal-api.azurewebsites.net/api/infinitepay/webhook
   ```
3. **Eventos para Monitorar**:
   - ✅ `payment.succeeded`
   - ✅ `payment.failed`
   - ✅ `payment.canceled`
4. **Salvar** e copiar o **Webhook Secret** (guardar para validação futura)

---

## 🧪 Testar Pagamento com Cartão

### **1. Acessar Dashboard**
```
https://gray-plant-08ef6cf0f.2.azurestaticapps.net
```

### **2. Click em "Receber Pagamento"**
- Selecione um projeto
- Click no botão **"💰 Receber"**

### **3. No Modal de Pagamento**
- Selecione aba **"Cartão"**
- Click **"Ir para Pagamento com Cartão"**

### **4. Use Cartões de Teste (Sandbox)**

✅ **Aprovado Imediatamente**:
```
Número: 4111 1111 1111 1111
CVV: 123
Validade: 12/28
Nome: Teste Aprovado
```

❌ **Negado (Teste de Erro)**:
```
Número: 5555 5555 5555 4444
CVV: 123
Validade: 12/28
Nome: Teste Negado
```

⏳ **Processamento Longo (Timeout)**:
```
Número: 3782 822463 10005
CVV: 1234
Validade: 12/28
Nome: Teste Timeout
```

---

## 📊 Monitorar Logs em Tempo Real

```powershell
# Ver logs das Functions
az monitor app-insights query `
  --resource-group rg-ativoreal-chile `
  --app func-ativoreal-api `
  --analytics-query "traces | order by timestamp desc | limit 50"

# Ou via portal
https://portal.azure.com/#resource/subscriptions/1f6ce75c-e8a7-4246-9225-b4ab1509c3a5/resourceGroups/rg-ativoreal-chile/providers/Microsoft.Web/sites/func-ativoreal-api/logStream
```

---

## 🔄 Atualizar Código Backend

Depois de fazer mudanças em `api/infinitepay_payment.py`:

```powershell
cd api
func azure functionapp publish func-ativoreal-api --python
```

---

## 💰 Custos Estimados

| Recurso | Custo Mensal |
|---------|--------------|
| **Function App** (Consumption) | ~R$ 0 a R$ 5 (1M execuções grátis) |
| **Storage Account** | ~R$ 1 (primeiros 5GB grátis) |
| **Static Web App** | **R$ 0** (Free tier) |
| **Application Insights** | ~R$ 5 (5GB logs grátis) |
| **InfinitePay Taxa** | 0.99% por transação |
| **TOTAL ESTIMADO** | **~R$ 10/mês + 0.99% por venda** |

---

## 🚀 Status Atual

✅ **Backend**: Publicado e funcionando  
✅ **Frontend**: Atualizado e deployado  
✅ **CORS**: Configurado  
✅ **Endpoints**: Testados (200 OK)  
⚠️ **API Key**: Precisa ser configurada (placeholder atual)  
⚠️ **Webhook**: Precisa ser registrado no InfinitePay  

---

## 🆘 Troubleshooting

### Erro: "Erro ao criar pagamento"
**Causa**: API Key inválida ou não configurada  
**Solução**: Atualizar `INFINITEPAY_API_KEY` no Azure Portal

### Erro: CORS bloqueado
**Causa**: Origin não permitido  
**Solução**: 
```powershell
az functionapp cors add --name func-ativoreal-api --resource-group rg-ativoreal-chile --allowed-origins "NOVA_URL"
```

### Erro: Timeout na API
**Causa**: Function App dormindo (cold start)  
**Solução**: Aguardar 10-15 segundos na primeira requisição

### Webhook não recebe notificações
**Causa**: URL não configurada no InfinitePay  
**Solução**: Configurar webhook no dashboard InfinitePay

---

## 📞 Próximos Passos

1. ✅ ~~Criar Function App~~ (FEITO)
2. ✅ ~~Publicar endpoints~~ (FEITO)
3. ✅ ~~Configurar CORS~~ (FEITO)
4. ✅ ~~Deploy frontend~~ (FEITO)
5. ⏳ **Você**: Obter API Key sandbox
6. ⏳ **Você**: Atualizar variável no Azure
7. ⏳ **Você**: Configurar webhook
8. 🧪 **Testar**: Cartão teste 4111 1111 1111 1111
9. 🎉 **Produção**: Trocar `sk_test_` por `sk_live_`

---

## 📚 Links Úteis

- **Function App**: https://portal.azure.com/#resource/subscriptions/1f6ce75c-e8a7-4246-9225-b4ab1509c3a5/resourceGroups/rg-ativoreal-chile/providers/Microsoft.Web/sites/func-ativoreal-api
- **Static Web App**: https://portal.azure.com/#resource/subscriptions/1f6ce75c-e8a7-4246-9225-b4ab1509c3a5/resourceGroups/rg-ativoreal-chile/providers/Microsoft.Web/staticSites/ativoreal-web-bfrrbwmkfi6xe
- **InfinitePay Dashboard**: https://dashboard.infinitepay.io
- **Documentação API**: https://docs.infinitepay.io
