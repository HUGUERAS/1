"""
Ativo Real - Azure Functions Backend
Migrado para Azure Cosmos DB NoSQL API + Redis Cache
"""

import azure.functions as func
import logging
import json
import os
from datetime import datetime, timedelta
import uuid
import hashlib
from azure.cosmos import CosmosClient, PartitionKey
import redis
from functools import wraps
from ai_assistant import get_ai_assistant

# Inicialização da Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# ========================================
# Configuração Cosmos DB
# ========================================
COSMOS_ENDPOINT = os.environ.get("COSMOS_DB_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_DB_KEY")
COSMOS_DATABASE = os.environ.get("COSMOS_DB_DATABASE", "AtivoRealDB")

cosmos_client = None
database = None

def get_cosmos_client():
    """Singleton Cosmos DB client"""
    global cosmos_client, database
    if cosmos_client is None:
        cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
        database = cosmos_client.get_database_client(COSMOS_DATABASE)
    return database

# ========================================
# Configuração Redis Cache
# ========================================
REDIS_CONN_STR = os.environ.get("REDIS_CONNECTION_STRING")
redis_client = None

def get_redis_client():
    """Singleton Redis client"""
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            f"redis://{REDIS_CONN_STR}",
            decode_responses=True,
            socket_timeout=5,
            socket_connect_timeout=5
        )
    return redis_client

# ========================================
# Decorators & Helpers
# ========================================

def require_fields(*required_fields):
    """Decorator para validar campos obrigatórios"""
    def decorator(func):
        @wraps(func)
        def wrapper(req: func.HttpRequest) -> func.HttpResponse:
            try:
                body = req.get_json()
            except ValueError:
                return func.HttpResponse(
                    json.dumps({"error": "Invalid JSON"}),
                    status_code=400,
                    mimetype="application/json"
                )
            
            missing = [f for f in required_fields if not body.get(f)]
            if missing:
                return func.HttpResponse(
                    json.dumps({"error": f"Missing fields: {', '.join(missing)}"}),
                    status_code=400,
                    mimetype="application/json"
                )
            
            return func(req, body)
        return wrapper
    return decorator

def cache_response(ttl_seconds=300):
    """Decorator para cache de respostas no Redis"""
    def decorator(func):
        @wraps(func)
        def wrapper(req: func.HttpRequest, *args, **kwargs):
            cache_key = f"{req.route_params.get('id', 'all')}:{req.url}"
            
            try:
                redis = get_redis_client()
                cached = redis.get(cache_key)
                if cached:
                    logging.info(f"Cache hit: {cache_key}")
                    return func.HttpResponse(
                        cached,
                        status_code=200,
                        mimetype="application/json"
                    )
            except Exception as e:
                logging.warning(f"Redis error: {e}")
            
            # Execute function
            response = func(req, *args, **kwargs)
            
            # Cache successful responses
            if response.status_code == 200:
                try:
                    redis = get_redis_client()
                    redis.setex(cache_key, ttl_seconds, response.get_body().decode())
                except Exception as e:
                    logging.warning(f"Failed to cache: {e}")
            
            return response
        return wrapper
    return decorator

def hash_password(password: str) -> str:
    """Hash password com SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def log_audit(tenant_id: str, user_id: str, action: str, resource: str, details: dict = None):
    """Registra log de auditoria no Cosmos DB"""
    try:
        db = get_cosmos_client()
        container = db.get_container_client("AuditLogs")
        
        log_entry = {
            "id": str(uuid.uuid4()),
            "tenantId": tenant_id,
            "userId": user_id,
            "action": action,
            "resource": resource,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat(),
            "ipAddress": None  # Pode ser extraído do request
        }
        
        container.create_item(log_entry)
    except Exception as e:
        logging.error(f"Failed to log audit: {e}")

# ========================================
# Health Check
# ========================================

@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    """Health check com status de serviços"""
    status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    # Check Cosmos DB
    try:
        db = get_cosmos_client()
        list(db.list_containers())
        status["services"]["cosmosdb"] = "connected"
    except Exception as e:
        status["services"]["cosmosdb"] = f"error: {str(e)}"
        status["status"] = "degraded"
    
    # Check Redis
    try:
        redis = get_redis_client()
        redis.ping()
        status["services"]["redis"] = "connected"
    except Exception as e:
        status["services"]["redis"] = f"error: {str(e)}"
    
    return func.HttpResponse(
        json.dumps(status),
        status_code=200,
        mimetype="application/json"
    )

# ========================================
# Rural Onboarding
# ========================================

@app.route(route="rural/onboard", methods=["POST"])
@require_fields("farmName", "document", "area", "adminName", "adminCpf")
def rural_onboard(req: func.HttpRequest, body: dict) -> func.HttpResponse:
    """Cadastro de propriedade rural"""
    logging.info("Cadastro rural iniciado")
    
    try:
        db = get_cosmos_client()
        container = db.get_container_client("RuralProperties")
        
        # Gerar IDs
        tenant_id = str(uuid.uuid4())
        property_id = str(uuid.uuid4())
        
        # Criar documento
        property_doc = {
            "id": property_id,
            "tenantId": tenant_id,
            "type": "rural",
            "farmName": body["farmName"],
            "document": body["document"],
            "area": float(body["area"]),
            "adminName": body["adminName"],
            "adminCpf": body["adminCpf"],
            "location": body.get("location"),  # GeoJSON Point ou Polygon
            "coordinates": body.get("coordinates", []),
            "status": "pending_validation",
            "createdAt": datetime.utcnow().isoformat(),
            "updatedAt": datetime.utcnow().isoformat()
        }
        
        # Salvar no Cosmos DB
        result = container.create_item(property_doc)
        
        # Log auditoria
        log_audit(tenant_id, "system", "CREATE", "RuralProperty", {
            "propertyId": property_id,
            "farmName": body["farmName"]
        })
        
        # Invalidar cache
        try:
            redis = get_redis_client()
            redis.delete("rural:list:*")
        except:
            pass
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "propertyId": property_id,
                "tenantId": tenant_id,
                "message": "Propriedade cadastrada com sucesso"
            }),
            status_code=201,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Erro no cadastro rural: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

# ========================================
# Urban Activation
# ========================================

@app.route(route="urban/activate", methods=["POST"])
@require_fields("cpf", "birthDate")
def urban_activate(req: func.HttpRequest, body: dict) -> func.HttpResponse:
    """Ativação de conta urbana"""
    logging.info("Ativação urbana iniciada")
    
    try:
        cpf = body["cpf"]
        birth_date = body["birthDate"]
        
        db = get_cosmos_client()
        users_container = db.get_container_client("Users")
        
        # Buscar usuário por CPF
        query = f"SELECT * FROM c WHERE c.cpf = '{cpf}'"
        users = list(users_container.query_items(query, enable_cross_partition_query=True))
        
        if not users:
            return func.HttpResponse(
                json.dumps({"error": "Usuário não encontrado"}),
                status_code=404,
                mimetype="application/json"
            )
        
        user = users[0]
        
        # Validar data de nascimento
        if user.get("birthDate") != birth_date:
            return func.HttpResponse(
                json.dumps({"error": "Data de nascimento incorreta"}),
                status_code=401,
                mimetype="application/json"
            )
        
        # Gerar token temporário ou senha
        activation_token = str(uuid.uuid4())
        
        # Atualizar usuário
        user["activationToken"] = activation_token
        user["activatedAt"] = datetime.utcnow().isoformat()
        user["status"] = "active"
        users_container.upsert_item(user)
        
        # Log auditoria
        log_audit(user["tenantId"], user["id"], "ACTIVATE", "User", {"cpf": cpf})
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "token": activation_token,
                "message": "Conta ativada com sucesso"
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Erro na ativação urbana: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

# ========================================
# Tech Login
# ========================================

@app.route(route="tech/login", methods=["POST"])
@require_fields("cpf", "password")
def tech_login(req: func.HttpRequest, body: dict) -> func.HttpResponse:
    """Login de técnico"""
    logging.info("Login de técnico")
    
    try:
        cpf = body["cpf"]
        password = body["password"]
        password_hash = hash_password(password)
        
        db = get_cosmos_client()
        users_container = db.get_container_client("Users")
        
        # Buscar técnico
        query = f"SELECT * FROM c WHERE c.cpf = '{cpf}' AND c.role = 'technician'"
        users = list(users_container.query_items(query, enable_cross_partition_query=True))
        
        if not users:
            return func.HttpResponse(
                json.dumps({"error": "Credenciais inválidas"}),
                status_code=401,
                mimetype="application/json"
            )
        
        user = users[0]
        
        # Verificar senha
        if user.get("passwordHash") != password_hash:
            return func.HttpResponse(
                json.dumps({"error": "Credenciais inválidas"}),
                status_code=401,
                mimetype="application/json"
            )
        
        # Gerar session token
        session_token = str(uuid.uuid4())
        
        # Cache session no Redis (24h)
        try:
            redis = get_redis_client()
            session_data = json.dumps({
                "userId": user["id"],
                "tenantId": user["tenantId"],
                "role": user["role"],
                "name": user.get("name")
            })
            redis.setex(f"session:{session_token}", 86400, session_data)
        except Exception as e:
            logging.warning(f"Failed to cache session: {e}")
        
        # Log auditoria
        log_audit(user["tenantId"], user["id"], "LOGIN", "User", {"cpf": cpf})
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "token": session_token,
                "user": {
                    "id": user["id"],
                    "name": user.get("name"),
                    "role": user["role"]
                }
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Erro no login: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

# ========================================
# List Properties (com geospatial query)
# ========================================

@app.route(route="properties", methods=["GET"])
@cache_response(ttl_seconds=300)
def list_properties(req: func.HttpRequest) -> func.HttpResponse:
    """Lista propriedades com filtro geoespacial opcional"""
    logging.info("Listando propriedades")
    
    try:
        # Parâmetros de query
        property_type = req.params.get("type")  # rural | urban
        lat = req.params.get("lat")
        lng = req.params.get("lng")
        radius_km = req.params.get("radius", "50")
        
        db = get_cosmos_client()
        
        # Container baseado no tipo
        container_name = "RuralProperties" if property_type == "rural" else "UrbanProperties"
        container = db.get_container_client(container_name)
        
        # Query geoespacial
        if lat and lng:
            query = f"""
                SELECT * FROM c
                WHERE ST_DISTANCE(c.location, {{
                    'type': 'Point',
                    'coordinates': [{lng}, {lat}]
                }}) < {float(radius_km) * 1000}
            """
        else:
            query = "SELECT * FROM c"
        
        items = list(container.query_items(
            query,
            enable_cross_partition_query=True,
            max_item_count=100
        ))
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "count": len(items),
                "properties": items
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Erro ao listar propriedades: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

# ========================================
# AI Assistant Endpoint
# ========================================

@app.route(route="ai/chat", methods=["POST"])
@require_fields("message")
def ai_chat(req: func.HttpRequest, body: dict) -> func.HttpResponse:
    """Chatbot AI com modelo fine-tuned"""
    logging.info("AI chat request")
    
    try:
        user_message = body["message"]
        context_type = body.get("context", "general")  # general | rural | urban
        conversation_id = body.get("conversationId")
        
        # Recuperar histórico do Redis (se existir)
        history = []
        if conversation_id:
            try:
                redis = get_redis_client()
                history_key = f"conversation:{conversation_id}"
                history_json = redis.get(history_key)
                if history_json:
                    history = json.loads(history_json)
            except Exception as e:
                logging.warning(f"Failed to retrieve conversation history: {e}")
        
        # Chamar AI Assistant
        assistant = get_ai_assistant()
        result = assistant.generate_response(
            user_message=user_message,
            context_type=context_type,
            conversation_history=history
        )
        
        if not result["success"]:
            return func.HttpResponse(
                json.dumps({
                    "error": "AI service unavailable",
                    "fallback": "Desculpe, o assistente está temporariamente indisponível."
                }),
                status_code=503,
                mimetype="application/json"
            )
        
        # Atualizar histórico
        if conversation_id:
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": result["response"]})
            
            try:
                redis = get_redis_client()
                redis.setex(
                    f"conversation:{conversation_id}",
                    3600,  # 1 hora
                    json.dumps(history[-10:])  # Últimas 10 mensagens
                )
            except Exception as e:
                logging.warning(f"Failed to save conversation history: {e}")
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "message": result["response"],
                "conversationId": conversation_id or str(uuid.uuid4()),
                "metadata": {
                    "model": result.get("model"),
                    "tokens": result.get("tokens_used"),
                    "timestamp": result.get("timestamp")
                }
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"AI chat error: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

