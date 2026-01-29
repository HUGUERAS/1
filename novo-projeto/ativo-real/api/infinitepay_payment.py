import azure.functions as func
import logging
import json
import os
import requests
from datetime import datetime

# Blueprint para InfinitePay
infinitepay_bp = func.Blueprint()

INFINITEPAY_API_KEY = os.environ.get('INFINITEPAY_API_KEY', '')
INFINITEPAY_BASE_URL = 'https://api.infinitepay.io/v1'

# ==================== 1. CRIAR PAGAMENTO ====================
@infinitepay_bp.route(route="infinitepay/create-payment", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def create_payment(req: func.HttpRequest) -> func.HttpResponse:
    """
    Cria um novo pagamento no InfinitePay.
    Body esperado: { "amount": 5000.00, "projectId": 123, "description": "Projeto XYZ" }
    """
    logging.info("InfinitePay: Criando novo pagamento")
    
    try:
        req_body = req.get_json()
        amount = req_body.get('amount')
        project_id = req_body.get('projectId')
        description = req_body.get('description', 'Pagamento Ativo Real')
        
        if not amount or not project_id:
            return func.HttpResponse(
                json.dumps({"error": "amount e projectId são obrigatórios"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Criar payload para InfinitePay
        payload = {
            "amount": int(amount * 100),  # Converter para centavos
            "currency": "BRL",
            "description": description,
            "payment_methods": ["pix", "credit_card", "boleto"],
            "metadata": {
                "project_id": str(project_id),
                "created_at": datetime.utcnow().isoformat()
            },
            "return_url": f"{os.environ.get('FRONTEND_URL', 'https://gray-plant-08ef6cr0f.2.azurestaticapps.net')}/dashboard",
            "webhook_url": f"{os.environ.get('FUNCTION_APP_URL', '')}/api/infinitepay/webhook"
        }
        
        # Chamar API InfinitePay
        headers = {
            "Authorization": f"Bearer {INFINITEPAY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{INFINITEPAY_BASE_URL}/payments",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 201:
            logging.error(f"InfinitePay API error: {response.status_code} - {response.text}")
            return func.HttpResponse(
                json.dumps({"error": "Erro ao criar pagamento", "details": response.text}),
                status_code=500,
                mimetype="application/json"
            )
        
        payment_data = response.json()
        
        # TODO: Salvar no Cosmos DB
        # cosmos_container.upsert_item({
        #     "id": payment_data['id'],
        #     "projectId": project_id,
        #     "status": payment_data['status'],
        #     "createdAt": datetime.utcnow().isoformat()
        # })
        
        logging.info(f"Pagamento criado: {payment_data['id']}")
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "paymentId": payment_data['id'],
                "status": payment_data['status'],
                "pixQrCode": payment_data.get('pix', {}).get('qr_code'),
                "pixCopyPaste": payment_data.get('pix', {}).get('copy_paste'),
                "checkoutUrl": payment_data.get('checkout_url'),
                "expiresAt": payment_data.get('expires_at')
            }),
            status_code=201,
            mimetype="application/json"
        )
        
    except ValueError as e:
        logging.error(f"JSON decode error: {e}")
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON payload"}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error creating payment: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


# ==================== 2. WEBHOOK ====================
@infinitepay_bp.route(route="infinitepay/webhook", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def infinitepay_webhook(req: func.HttpRequest) -> func.HttpResponse:
    """
    Recebe notificações do InfinitePay sobre mudanças no status do pagamento.
    """
    logging.info("InfinitePay: Webhook recebido")
    
    try:
        req_body = req.get_json()
        event_type = req_body.get('event')
        payment_data = req_body.get('data', {})
        
        payment_id = payment_data.get('id')
        status = payment_data.get('status')
        project_id = payment_data.get('metadata', {}).get('project_id')
        
        logging.info(f"Webhook - Event: {event_type}, Payment: {payment_id}, Status: {status}")
        
        # TODO: Atualizar Cosmos DB
        # if event_type == 'payment.succeeded':
        #     cosmos_container.patch_item(
        #         item=payment_id,
        #         partition_key=project_id,
        #         patch_operations=[
        #             {"op": "replace", "path": "/status", "value": "paid"},
        #             {"op": "set", "path": "/paidAt", "value": datetime.utcnow().isoformat()}
        #         ]
        #     )
        
        # Eventos possíveis:
        # - payment.created
        # - payment.pending
        # - payment.succeeded (PAGO!)
        # - payment.failed
        # - payment.expired
        
        if event_type == 'payment.succeeded':
            logging.info(f"✅ Pagamento {payment_id} confirmado para projeto {project_id}")
            # Aqui você pode enviar email, atualizar projeto, etc.
        
        return func.HttpResponse(
            json.dumps({"received": True}),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


# ==================== 3. VERIFICAR STATUS ====================
@infinitepay_bp.route(route="infinitepay/check-status/{payment_id}", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def check_payment_status(req: func.HttpRequest) -> func.HttpResponse:
    """
    Verifica o status atual de um pagamento.
    """
    payment_id = req.route_params.get('payment_id')
    logging.info(f"InfinitePay: Verificando status do pagamento {payment_id}")
    
    try:
        headers = {
            "Authorization": f"Bearer {INFINITEPAY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{INFINITEPAY_BASE_URL}/payments/{payment_id}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            return func.HttpResponse(
                json.dumps({"error": "Pagamento não encontrado"}),
                status_code=404,
                mimetype="application/json"
            )
        
        payment_data = response.json()
        
        return func.HttpResponse(
            json.dumps({
                "paymentId": payment_data['id'],
                "status": payment_data['status'],
                "amount": payment_data['amount'] / 100,  # Converter centavos para reais
                "createdAt": payment_data.get('created_at'),
                "paidAt": payment_data.get('paid_at'),
                "method": payment_data.get('payment_method')
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error checking payment status: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
