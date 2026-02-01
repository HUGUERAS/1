# Agent 4: Payment Integration Engineer - InfinitePay

## Mission
Implement and validate InfinitePay payment integration for lot clients:
1. Create payment requests (PIX, Boleto, Credit Card)
2. Handle async payment webhooks
3. Update lot status on successful payment (PENDENTE → PAGO)
4. Retry logic for failed payments
5. Compliance with PCI/fraud prevention

## Deliverables
1. **Payment API Endpoint**: POST `/api/payments/infinitepay`
2. **Webhook Handler**: POST `/api/payments/webhook/infinitepay`
3. **Payment Status Checker**: GET `/api/payments/{id}/status`
4. **InfinitePay Integration Module**: Reusable client
5. **Test Suite**: Webhook simulation, error scenarios

## Business Flow
1. **Client clicks "Pay"** on portal
   - Lot ID, valor_total from database
   - Create payment record in `payments` table (status: PENDENTE)
   
2. **Request to InfinitePay**
   - API call: `POST https://api.infinitepay.io/charge`
   - Payload: lot_id, valor_total, customer_email, return_url
   - Response: gateway_id, payment_url
   
3. **Client redirects to InfinitePay**
   - User selects PIX/Boleto/Card
   - Completes payment
   
4. **Webhook callback** (async)
   - InfinitePay calls: `POST /api/payments/webhook/infinitepay`
   - Body: gateway_id, status, timestamp, signature
   - Verify HMAC signature (security)
   - Update `payments.status` (APROVADO|RECUSADO)
   - Update `lots.status` (PAGO) if payment approved
   - Send email/SMS confirmation to client

5. **Client portal shows status**
   - Polling endpoint: GET `/api/lots/{token}/status`
   - Returns: payment status, lot status, next steps

## Database Schema Integration
```sql
payments (
    id UUID,
    lot_id UUID,           -- FK to lots
    valor_total DECIMAL,
    status ENUM,           -- PENDENTE|PROCESSANDO|APROVADO|RECUSADO|REEMBOLSADO
    gateway_id VARCHAR,    -- InfinitePay ID
    gateway_resposta JSONB -- Full webhook response
)

lots (
    status ENUM            -- PENDENTE|PAGO|PROCESSANDO|FINALIZADO|CANCELADO
)
```

## API Details

### Create Payment
```
POST /api/payments/create
{
    "lot_id": "uuid",
    "valor_total": 1500.00,
    "customer_email": "cliente@email.com",
    "customer_phone": "11987654321"
}

Response:
{
    "payment_id": "uuid",
    "gateway_id": "inf_xxxxx",
    "payment_url": "https://infinitepay.io/checkout/...",
    "expires_at": "2026-02-01T12:00:00Z"
}
```

### Webhook Handler
```
POST /api/payments/webhook/infinitepay
{
    "gateway_id": "inf_xxxxx",
    "status": "approved",
    "amount": 1500.00,
    "timestamp": "2026-01-31T10:30:00Z",
    "signature": "hmac_sha256..."
}
```

### Status Checker
```
GET /api/payments/{payment_id}/status

Response:
{
    "payment_id": "uuid",
    "lot_id": "uuid",
    "status": "approved",
    "valor_pago": 1500.00,
    "lot_status": "pago",
    "updated_at": "2026-01-31T10:30:00Z"
}
```

## Security Requirements
1. **HMAC Signature Verification**: All webhooks must be validated with shared secret
2. **Idempotency**: Handle duplicate webhook calls (check gateway_id)
3. **Rate Limiting**: Prevent payment spam on same lot
4. **Logging**: Log all payment events for audit trail
5. **Error Handling**: Never expose InfinitePay API keys in responses

## Error Scenarios
- ❌ Invalid lot_id → 404
- ❌ Lot already PAGO → 409 Conflict
- ❌ InfinitePay API timeout → 503 Service Unavailable
- ❌ Bad HMAC signature → 401 Unauthorized (reject webhook)
- ❌ Webhook replay attack → Idempotency check (201 Created or 200 OK)

## Testing
- **Unit Tests**: HMAC verification, status transitions
- **Integration Tests**: Mock InfinitePay API responses
- **E2E Tests**: Full payment flow on staging SWA

## Deployment Notes
- Store `INFINITEPAY_API_KEY` in Azure Key Vault
- Store `INFINITEPAY_WEBHOOK_SECRET` in Azure Key Vault
- Webhook endpoint public (no auth required for InfinitePay)
- All responses must be JSON + CORS headers
