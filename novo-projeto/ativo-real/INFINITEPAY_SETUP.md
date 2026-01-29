# 🚀 Configuração InfinitePay - Ativo Real

## ✅ Status da Implementação

### Frontend (COMPLETO ✓)
- ✅ Componente `InfinitePayModal.tsx` criado
- ✅ Estilos `InfinitePayModal.css` criados
- ✅ Integração no `DashboardTopografo.tsx`
- ✅ Build e deploy realizados
- 🌐 URL: https://gray-plant-08ef6cf0f.2.azurestaticapps.net

### Backend (PENDENTE CONFIGURAÇÃO)
- ✅ Código criado: `api/infinitepay_payment.py`
- ✅ Blueprint registrado em `function_app.py`
- ✅ Biblioteca `requests` adicionada ao `requirements.txt`
- ⚠️ **PENDENTE**: Publicação no Azure Functions
- ⚠️ **PENDENTE**: Configuração de variáveis de ambiente

---

## 📋 Próximos Passos (VOCÊ PRECISA FAZER)

### 1️⃣ Obter Credenciais InfinitePay

1. Acesse: https://infinitepay.io/
2. Crie uma conta ou faça login
3. Acesse **Desenvolvedor > API Keys**
4. Copie a **API Key de Produção** ou **Sandbox** (para testes)
5. Guarde a chave em local seguro

**Formato esperado:**
```
ipay_sk_live_abc123def456ghi789jkl012mno345
```

### 2️⃣ Configurar Azure Functions (Variáveis de Ambiente)

Você precisa adicionar as seguintes variáveis nas **Application Settings** do seu Azure Function App:

#### Via Azure Portal:
1. Acesse: https://portal.azure.com
2. Navegue para: **Azure Functions** > `[SEU FUNCTION APP]`
3. Menu lateral: **Configuration** > **Application settings**
4. Clique em **+ New application setting** para cada variável abaixo:

| Nome da Variável | Valor | Descrição |
|------------------|-------|-----------|
| `INFINITEPAY_API_KEY` | `ipay_sk_live_...` | Chave da API InfinitePay |
| `FRONTEND_URL` | `https://gray-plant-08ef6cf0f.2.azurestaticapps.net` | URL do frontend (para return_url) |
| `FUNCTION_APP_URL` | `https://[SEU-FUNCTION-APP].azurewebsites.net` | URL do backend (para webhook) |

#### Via Azure CLI (Alternativa):
```bash
# Substitua os valores entre <>
az functionapp config appsettings set \
  --name <NOME_DO_FUNCTION_APP> \
  --resource-group rg-ativoreal-chile \
  --settings \
    "INFINITEPAY_API_KEY=ipay_sk_live_abc123..." \
    "FRONTEND_URL=https://gray-plant-08ef6cf0f.2.azurestaticapps.net" \
    "FUNCTION_APP_URL=https://<NOME_DO_FUNCTION_APP>.azurewebsites.net"
```

### 3️⃣ Publicar o Backend no Azure

**Pré-requisitos:**
- Azure Functions Core Tools instalado
- Azure CLI autenticado (`az login`)

**Comandos para deploy:**

```powershell
# 1. Navegar para a pasta da API
cd C:\Users\huugo\topdemais\ativo-real\api

# 2. Instalar dependências localmente (teste)
pip install -r requirements.txt

# 3. Publicar no Azure (substitua <FUNCTION_APP_NAME>)
func azure functionapp publish <FUNCTION_APP_NAME> --python

# Exemplo:
# func azure functionapp publish ativoreal-functions --python
```

**Nota:** Se você não tiver um Function App criado ainda, precisa criar primeiro:

```bash
# Criar Function App
az functionapp create \
  --name ativoreal-functions \
  --resource-group rg-ativoreal-chile \
  --consumption-plan-location eastus2 \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --storage-account <NOME_STORAGE_ACCOUNT>
```

### 4️⃣ Configurar Webhook no InfinitePay

1. Acesse o painel InfinitePay: https://dashboard.infinitepay.io
2. Vá em **Configurações > Webhooks**
3. Adicione um novo webhook:
   - **URL**: `https://<FUNCTION_APP_NAME>.azurewebsites.net/api/infinitepay/webhook`
   - **Eventos**: Selecione:
     - ✅ `payment.created`
     - ✅ `payment.succeeded` (MAIS IMPORTANTE)
     - ✅ `payment.failed`
     - ✅ `payment.expired`
4. Salve e teste o webhook

### 5️⃣ Testar a Integração

#### Teste Manual (Frontend):
1. Acesse: https://gray-plant-08ef6cf0f.2.azurestaticapps.net
2. Login como Topógrafo
3. Vá para aba **💰 Financeiro**
4. Clique em **💳 Online** em algum projeto com valor pendente
5. Verifique se o modal abre e mostra opções PIX/Cartão/Boleto

#### Teste Backend (curl):
```bash
# Testar criação de pagamento
curl -X POST https://<FUNCTION_APP_NAME>.azurewebsites.net/api/infinitepay/create-payment \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000.00,
    "projectId": 123,
    "description": "Teste"
  }'

# Resposta esperada (sucesso):
{
  "success": true,
  "paymentId": "ipay_abc123...",
  "status": "pending",
  "pixQrCode": "data:image/png;base64,...",
  "pixCopyPaste": "00020126...",
  "checkoutUrl": "https://checkout.infinitepay.io/...",
  "expiresAt": "2026-01-22T23:00:00Z"
}
```

#### Verificar Logs (Azure Portal):
1. Acesse: **Function App** > **Log stream**
2. Execute um pagamento pelo frontend
3. Observe os logs em tempo real

---

## 🛠️ Troubleshooting

### Erro: "INFINITEPAY_API_KEY não definida"
**Solução:** Configure a variável de ambiente no Azure Portal (passo 2️⃣)

### Erro: "Failed to fetch" ou CORS
**Solução:** Verifique se o Function App permite CORS do frontend:
```bash
az functionapp cors add \
  --name <FUNCTION_APP_NAME> \
  --resource-group rg-ativoreal-chile \
  --allowed-origins https://gray-plant-08ef6cf0f.2.azurestaticapps.net
```

### Webhook não está sendo chamado
**Soluções:**
1. Verifique se a URL do webhook está correta no painel InfinitePay
2. Confirme que a `FUNCTION_APP_URL` está configurada
3. Teste manualmente via curl:
```bash
curl -X POST https://<FUNCTION_APP_NAME>.azurewebsites.net/api/infinitepay/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "payment.succeeded",
    "data": {
      "id": "test123",
      "status": "succeeded",
      "metadata": {"project_id": "1"}
    }
  }'
```

### Pagamento PIX não atualiza automaticamente
**Motivo:** O polling está rodando a cada 3 segundos no frontend, mas precisa do backend funcionando
**Solução:** Publique o backend e configure as variáveis de ambiente

---

## 📊 Endpoints Criados

### 1. Criar Pagamento
- **URL**: `POST /api/infinitepay/create-payment`
- **Body**:
  ```json
  {
    "amount": 5000.00,
    "projectId": 123,
    "description": "Pagamento Projeto XYZ"
  }
  ```
- **Resposta**:
  ```json
  {
    "success": true,
    "paymentId": "ipay_...",
    "status": "pending",
    "pixQrCode": "data:image/png;base64,...",
    "pixCopyPaste": "00020126...",
    "checkoutUrl": "https://...",
    "expiresAt": "2026-01-22T..."
  }
  ```

### 2. Webhook (recebe notificações)
- **URL**: `POST /api/infinitepay/webhook`
- **Chamado automaticamente pelo InfinitePay**
- **Eventos**: `payment.created`, `payment.succeeded`, `payment.failed`, `payment.expired`

### 3. Verificar Status
- **URL**: `GET /api/infinitepay/check-status/{payment_id}`
- **Resposta**:
  ```json
  {
    "paymentId": "ipay_...",
    "status": "succeeded",
    "amount": 5000.00,
    "createdAt": "2026-01-22T...",
    "paidAt": "2026-01-22T...",
    "method": "pix"
  }
  ```

---

## 💰 Taxas InfinitePay

| Método | Taxa |
|--------|------|
| PIX | **0.99%** |
| Cartão de Crédito | **0.99%** + R$ 0,40 |
| Boleto | **R$ 3,49** por boleto |

**Exemplo de cálculo:**
- Projeto de R$ 5.000,00 pago via PIX
- Taxa: R$ 5.000,00 × 0.99% = **R$ 49,50**
- Você recebe: **R$ 4.950,50**

---

## 📝 Checklist Final

Antes de usar em produção, confirme:

- [ ] API Key da InfinitePay obtida
- [ ] Variáveis de ambiente configuradas no Azure Functions
- [ ] Backend publicado no Azure (`func azure functionapp publish`)
- [ ] Webhook configurado no painel InfinitePay
- [ ] CORS habilitado no Function App
- [ ] Teste de pagamento PIX realizado com sucesso
- [ ] Teste de webhook realizado (verificar logs)
- [ ] Frontend acessível em https://gray-plant-08ef6cf0f.2.azurestaticapps.net

---

## 🎯 Próximas Melhorias (Futuro)

1. **Cosmos DB Integration**: Salvar pagamentos no banco (comentado no código)
2. **Email Notifications**: Enviar confirmação de pagamento por email
3. **Relatórios**: Dashboard com histórico de transações
4. **Webhooks Retry**: Implementar retry automático para webhooks falhados
5. **Multi-tenant**: Separar taxas por topógrafo

---

## 📞 Suporte

- **InfinitePay Docs**: https://docs.infinitepay.io/
- **Azure Functions Docs**: https://learn.microsoft.com/azure/azure-functions/
- **GitHub Copilot**: Para dúvidas sobre o código

---

**Última atualização:** 22/01/2026
**Status:** ✅ Frontend deployado | ⚠️ Backend aguardando configuração
