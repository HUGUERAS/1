"""
🔐 Middleware de Autenticação JWT para Azure Functions
Sistema completo de autenticação com JWT, RBAC e gestão de sessões

Autor: GitHub Copilot - Refatoração Single-Page
Data: 31/01/2026
"""

import jwt
import os
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Optional, Callable
import json

# =====================================================
# CONFIGURAÇÕES
# =====================================================

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE-THIS-SECRET-KEY-IN-PRODUCTION-USE-LONG-RANDOM-STRING")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Roles disponíveis (sincronizado com enum do PostgreSQL)
class UserRole:
    ADMIN = "ADMIN"
    TOPOGRAFO = "TOPOGRAFO"
    CLIENTE = "CLIENTE"
    AGRICULTOR = "AGRICULTOR"
    
    @classmethod
    def all(cls):
        return [cls.ADMIN, cls.TOPOGRAFO, cls.CLIENTE, cls.AGRICULTOR]


# =====================================================
# FUNÇÕES DE TOKEN
# =====================================================

def create_access_token(user_id: int, role: str, email: str) -> str:
    """
    Cria JWT access token
    
    Args:
        user_id: ID do usuário
        role: Role do usuário (ADMIN, TOPOGRAFO, CLIENTE, AGRICULTOR)
        email: Email do usuário
        
    Returns:
        Token JWT assinado
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_id": user_id,
        "role": role,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: int, role: str, email: str) -> str:
    """
    Cria JWT refresh token (validade de 7 dias)
    
    Args:
        user_id: ID do usuário
        role: Role do usuário
        email: Email do usuário
        
    Returns:
        Refresh token JWT assinado
    """
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "user_id": user_id,
        "role": role,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Dict:
    """
    Verifica e decodifica JWT
    
    Args:
        token: Token JWT a ser verificado
        
    Returns:
        Payload do token decodificado
        
    Raises:
        ValueError: Se token for inválido ou expirado
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")


def hash_refresh_token(token: str) -> str:
    """
    Cria hash SHA256 do refresh token para armazenamento seguro
    
    Args:
        token: Refresh token em plain text
        
    Returns:
        Hash SHA256 do token
    """
    return hashlib.sha256(token.encode()).hexdigest()


# =====================================================
# DECORATORS DE AUTENTICAÇÃO
# =====================================================

def require_auth(func: Callable) -> Callable:
    """
    Decorator para proteger endpoints com autenticação JWT
    
    Adiciona os seguintes atributos ao request:
    - req.user_id: ID do usuário autenticado
    - req.user_role: Role do usuário
    - req.user_email: Email do usuário
    
    Uso:
        @app.route(route="projetos", methods=["GET"])
        @require_auth
        def listar_projetos(req: func.HttpRequest) -> func.HttpResponse:
            user_id = req.user_id
            role = req.user_role
            # ...
    """
    @wraps(func)
    def wrapper(req: func.HttpRequest, *args, **kwargs) -> func.HttpResponse:
        # Extrair token do header Authorization
        auth_header = req.headers.get("Authorization", "")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return func.HttpResponse(
                json.dumps({
                    "error": "Token de autenticação não fornecido",
                    "code": "AUTH_TOKEN_MISSING"
                }),
                status_code=401,
                mimetype="application/json",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        token = auth_header.split(" ")[1]
        
        try:
            # Verificar e decodificar token
            payload = verify_token(token)
            
            # Validar tipo de token
            if payload.get("type") != "access":
                raise ValueError("Tipo de token inválido")
            
            # Adicionar informações do usuário ao request
            req.user_id = payload["user_id"]
            req.user_role = payload["role"]
            req.user_email = payload.get("email", "")
            
            # Chamar função original
            return func(req, *args, **kwargs)
            
        except ValueError as e:
            return func.HttpResponse(
                json.dumps({
                    "error": str(e),
                    "code": "AUTH_TOKEN_INVALID"
                }),
                status_code=401,
                mimetype="application/json",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except Exception as e:
            return func.HttpResponse(
                json.dumps({
                    "error": "Erro ao processar token",
                    "code": "AUTH_ERROR",
                    "details": str(e)
                }),
                status_code=500,
                mimetype="application/json"
            )
    
    return wrapper


def require_role(*allowed_roles: str) -> Callable:
    """
    Decorator para verificar role do usuário (RBAC)
    
    DEVE ser usado APÓS @require_auth
    
    Args:
        *allowed_roles: Roles permitidas (ADMIN, TOPOGRAFO, CLIENTE, AGRICULTOR)
        
    Uso:
        @app.route(route="admin/users", methods=["GET"])
        @require_auth
        @require_role(UserRole.ADMIN)
        def listar_usuarios(req: func.HttpRequest):
            # Apenas ADMIN pode acessar
            pass
            
        @app.route(route="projetos", methods=["POST"])
        @require_auth
        @require_role(UserRole.ADMIN, UserRole.TOPOGRAFO)
        def criar_projeto(req: func.HttpRequest):
            # ADMIN e TOPOGRAFO podem criar projetos
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(req: func.HttpRequest, *args, **kwargs) -> func.HttpResponse:
            # Verificar se usuário foi autenticado
            if not hasattr(req, 'user_role'):
                return func.HttpResponse(
                    json.dumps({
                        "error": "Usuário não autenticado",
                        "code": "AUTH_REQUIRED"
                    }),
                    status_code=401,
                    mimetype="application/json"
                )
            
            # Verificar se role está nas permitidas
            if req.user_role not in allowed_roles:
                return func.HttpResponse(
                    json.dumps({
                        "error": "Permissão negada",
                        "code": "PERMISSION_DENIED",
                        "required_roles": list(allowed_roles),
                        "user_role": req.user_role
                    }),
                    status_code=403,
                    mimetype="application/json"
                )
            
            return func(req, *args, **kwargs)
        
        return wrapper
    return decorator


def optional_auth(func: Callable) -> Callable:
    """
    Decorator para endpoints que aceitam autenticação opcional
    
    Se token estiver presente e válido, adiciona user_id/role ao request
    Se token não estiver presente ou for inválido, continua sem autenticação
    
    Uso:
        @app.route(route="planos", methods=["GET"])
        @optional_auth
        def listar_planos(req: func.HttpRequest):
            if hasattr(req, 'user_id'):
                # Usuário autenticado - mostrar planos personalizados
                pass
            else:
                # Usuário não autenticado - mostrar planos públicos
                pass
    """
    @wraps(func)
    def wrapper(req: func.HttpRequest, *args, **kwargs) -> func.HttpResponse:
        auth_header = req.headers.get("Authorization", "")
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
            try:
                payload = verify_token(token)
                
                if payload.get("type") == "access":
                    req.user_id = payload["user_id"]
                    req.user_role = payload["role"]
                    req.user_email = payload.get("email", "")
            except:
                pass  # Ignora erro de token inválido
        
        return func(req, *args, **kwargs)
    
    return wrapper


# =====================================================
# HELPERS PARA VALIDAÇÃO
# =====================================================

def is_admin(req: func.HttpRequest) -> bool:
    """Verifica se usuário é ADMIN"""
    return hasattr(req, 'user_role') and req.user_role == UserRole.ADMIN


def is_topografo(req: func.HttpRequest) -> bool:
    """Verifica se usuário é TOPOGRAFO"""
    return hasattr(req, 'user_role') and req.user_role == UserRole.TOPOGRAFO


def can_manage_projects(req: func.HttpRequest) -> bool:
    """Verifica se usuário pode gerenciar projetos (ADMIN ou TOPOGRAFO)"""
    return hasattr(req, 'user_role') and req.user_role in [UserRole.ADMIN, UserRole.TOPOGRAFO]


def get_user_info(req: func.HttpRequest) -> Optional[Dict]:
    """
    Retorna informações do usuário autenticado
    
    Returns:
        Dict com user_id, role e email ou None se não autenticado
    """
    if hasattr(req, 'user_id'):
        return {
            "user_id": req.user_id,
            "role": req.user_role,
            "email": req.user_email
        }
    return None


# =====================================================
# UTILITÁRIOS DE REQUEST
# =====================================================

def get_client_ip(req: func.HttpRequest) -> str:
    """
    Extrai IP do cliente do request
    
    Verifica headers X-Forwarded-For e X-Real-IP (Azure/proxy)
    """
    forwarded = req.headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0].strip()
    
    real_ip = req.headers.get('X-Real-IP')
    if real_ip:
        return real_ip
    
    return req.headers.get('REMOTE_ADDR', 'unknown')


def get_user_agent(req: func.HttpRequest) -> str:
    """Extrai User-Agent do request"""
    return req.headers.get('User-Agent', 'unknown')


# =====================================================
# EXEMPLO DE USO
# =====================================================

if __name__ == "__main__":
    # Exemplo de criação de tokens
    test_user_id = 1
    test_role = UserRole.ADMIN
    test_email = "admin@ativoreal.com.br"
    
    access = create_access_token(test_user_id, test_role, test_email)
    refresh = create_refresh_token(test_user_id)
    
    print("=" * 60)
    print("🔐 EXEMPLO DE TOKENS JWT")
    print("=" * 60)
    print(f"\n📝 Access Token (válido por {ACCESS_TOKEN_EXPIRE_MINUTES} minutos):")
    print(access)
    print(f"\n🔄 Refresh Token (válido por {REFRESH_TOKEN_EXPIRE_DAYS} dias):")
    print(refresh)
    
    # Verificar token
    try:
        payload = verify_token(access)
        print(f"\n✅ Token válido!")
        print(f"User ID: {payload['user_id']}")
        print(f"Role: {payload['role']}")
        print(f"Email: {payload['email']}")
        print(f"Expira em: {datetime.fromtimestamp(payload['exp'])}")
    except ValueError as e:
        print(f"\n❌ Erro: {e}")
    
    print("\n" + "=" * 60)
