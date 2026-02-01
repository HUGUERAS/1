"""
Agent 4: Payment Integration - InfinitePay Handler
File: novo-projeto/backend/infinitepay_handler.py
"""

import hmac
import hashlib
import json
import logging
from datetime import datetime
from decimal import Decimal
import azure.functions as func
from database import SessionLocal
import models
import schemas
from sqlalchemy import update

logger = logging.getLogger("infinitepay")

class InfinitePayHandler:
    """
    Handles InfinitePay payment webhook and integration
    """
    
    def __init__(self, api_key: str = None, webhook_secret: str = None):
        self.api_key = api_key or ""
        self.webhook_secret = webhook_secret or ""
    
    def verify_signature(self, payload: str, signature: str) -> bool:
        """
        Verify HMAC signature from InfinitePay webhook
        
        Args:
            payload: Raw JSON payload
            signature: HMAC signature from header
            
        Returns:
            True if signature valid, False otherwise
        """
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def handle_webhook(self, db, payload: dict) -> dict:
        """
        Handle InfinitePay webhook callback
        
        Expected payload:
        {
            "gateway_id": "inf_xxxxx",
            "status": "approved|pending|rejected",
            "amount": 1500.00,
            "lot_id": "uuid",
            "timestamp": "2026-01-31T10:30:00Z",
            "signature": "hmac_..."
        }
        """
        
        try:
            gateway_id = payload.get('gateway_id')
            status = payload.get('status')  # approved, pending, rejected
            lot_id = payload.get('lot_id')
            amount = Decimal(str(payload.get('amount', 0)))
            
            # Idempotency check: Don't process same payment twice
            existing_payment = db.query(models.Payment).filter(
                models.Payment.gateway_id == gateway_id
            ).first()
            
            if existing_payment:
                logger.warning(f"Duplicate webhook: {gateway_id}")
                return {
                    "status": "duplicate",
                    "message": "Payment already processed"
                }
            
            # Find lot
            lot = db.query(models.Lot).filter(
                models.Lot.id == lot_id
            ).first()
            
            if not lot:
                logger.error(f"Lot not found: {lot_id}")
                return {"status": "error", "message": "Lot not found"}
            
            # Create payment record
            payment_status_map = {
                "approved": "APROVADO",
                "pending": "PROCESSANDO",
                "rejected": "RECUSADO"
            }
            
            payment = models.Payment(
                lot_id=lot_id,
                valor_total=amount,
                valor_pago=amount if status == "approved" else Decimal(0),
                status=payment_status_map.get(status, "PENDENTE"),
                gateway_id=gateway_id,
                gateway_resposta=json.dumps(payload)
            )
            
            db.add(payment)
            
            # Update lot status if payment approved
            if status == "approved":
                lot.status = "PAGO"
                logger.info(f"Lot {lot_id} marked as PAGO")
                
                # Send confirmation email (future implementation)
                # send_email_confirmation(lot.email_cliente, lot.nome_cliente)
            
            db.commit()
            
            logger.info(f"Payment processed: {gateway_id} - {status}")
            
            return {
                "status": "success",
                "payment_id": str(payment.id),
                "lot_status": lot.status
            }
        
        except Exception as e:
            db.rollback()
            logger.error(f"Webhook error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def create_payment_request(self, lot_id: str, valor_total: float, customer_email: str, db) -> dict:
        """
        Create payment request and get checkout URL
        
        Returns:
        {
            "payment_id": "uuid",
            "gateway_id": "inf_xxxxx",
            "payment_url": "https://checkout.infinitepay.io/...",
            "expires_at": "2026-02-01T12:00:00Z"
        }
        """
        
        try:
            # Create payment record with PENDENTE status
            payment = models.Payment(
                lot_id=lot_id,
                valor_total=Decimal(str(valor_total)),
                status="PENDENTE",
                gateway_resposta=json.dumps({
                    "created_at": datetime.utcnow().isoformat(),
                    "customer_email": customer_email
                })
            )
            
            db.add(payment)
            db.commit()
            
            # Mock InfinitePay API call (in production, call actual API)
            # response = requests.post('https://api.infinitepay.io/charges', {...})
            
            # For MVP, return mock response
            gateway_id = f"inf_{payment.id.hex[:8]}"
            payment_url = f"https://checkout.infinitepay.io/pay/{gateway_id}"
            
            # Update payment with gateway_id
            db.execute(
                update(models.Payment).where(
                    models.Payment.id == payment.id
                ).values(gateway_id=gateway_id)
            )
            db.commit()
            
            logger.info(f"Payment created: {payment.id} for lot {lot_id}")
            
            return {
                "payment_id": str(payment.id),
                "gateway_id": gateway_id,
                "payment_url": payment_url,
                "expires_at": "2026-02-01T12:00:00Z"
            }
        
        except Exception as e:
            db.rollback()
            logger.error(f"Payment creation error: {str(e)}")
            raise


# Azure Functions Endpoint
def create_payment_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """
    POST /api/payments/create
    Create new payment request
    """
    
    try:
        req_body = req.get_json()
        lot_id = req_body.get('lot_id')
        valor_total = req_body.get('valor_total')
        customer_email = req_body.get('customer_email')
        
        db = SessionLocal()
        handler = InfinitePayHandler()
        
        result = handler.create_payment_request(
            lot_id=lot_id,
            valor_total=valor_total,
            customer_email=customer_email,
            db=db
        )
        
        db.close()
        
        return func.HttpResponse(
            body=json.dumps(result),
            status_code=201,
            mimetype="application/json"
        )
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json"
        )


def webhook_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """
    POST /api/payments/webhook/infinitepay
    Handle InfinitePay webhook callback
    """
    
    try:
        # Get signature from header
        signature = req.headers.get('X-InfinitePay-Signature', '')
        payload_str = req.get_body().decode()
        payload = json.loads(payload_str)
        
        # Verify signature
        handler = InfinitePayHandler(
            webhook_secret="your_webhook_secret"  # From env variables
        )
        
        if not handler.verify_signature(payload_str, signature):
            logger.warning("Invalid webhook signature")
            return func.HttpResponse(
                body=json.dumps({"error": "Invalid signature"}),
                status_code=401,
                mimetype="application/json"
            )
        
        # Process webhook
        db = SessionLocal()
        result = handler.handle_webhook(db, payload)
        db.close()
        
        status_code = 200 if result['status'] == 'success' else 400
        
        return func.HttpResponse(
            body=json.dumps(result),
            status_code=status_code,
            mimetype="application/json"
        )
    
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json"
        )
