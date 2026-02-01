import azure.functions as func
import logging
import json
import os
from datetime import datetime, timedelta
from database import SessionLocal, engine
import models
import schemas
import logic_services
from pydantic import ValidationError
from auth_middleware import (
    create_access_token, 
    create_refresh_token, 
    verify_token, 
    require_auth, 
    require_role
)
from sqlalchemy.exc import IntegrityError
from openrouter_client import (
    get_openrouter_client,
    handle_openrouter_error,
    OpenRouterClient
)

# Comentado para evitar crash no startup - tabelas ja criadas via script
# models.Base.metadata.create_all(bind=engine)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# ==================== AUTH ENDPOINTS ====================

@app.route(route="auth/login", methods=["POST"])
def login(req: func.HttpRequest) -> func.HttpResponse:
    """
    Endpoint de login - valida credenciais e retorna tokens JWT
    
    Request Body:
    {
        "email": "user@example.com",
        "password": "senha123"
    }
    
    Response:
    {
        "access_token": "eyJ...",
        "refresh_token": "eyJ...",
        "token_type": "Bearer",
        "expires_in": 1800,
        "user": {...}
    }
    """
    logging.info("🔐 Login request recebido")
    
    try:
        req_body = req.get_json()
        login_data = schemas.LoginRequest(**req_body)
    except ValidationError as e:
        return func.HttpResponse(
            body=json.dumps({"error": "Dados inválidos", "details": e.errors()}),
            status_code=400,
            mimetype="application/json"
        )
    except ValueError:
        return func.HttpResponse(
            body=json.dumps({"error": "JSON inválido"}),
            status_code=400,
            mimetype="application/json"
        )
    
    db = SessionLocal()
    try:
        # Busca usuário por email
        user = db.query(models.User).filter(models.User.email == login_data.email).first()
        
        if not user:
            logging.warning(f"❌ Login falhou - email não encontrado: {login_data.email}")
            return func.HttpResponse(
                body=json.dumps({"error": "Credenciais inválidas"}),
                status_code=401,
                mimetype="application/json"
            )
        
        # Valida senha
        if not user.check_password(login_data.password):
            logging.warning(f"❌ Login falhou - senha incorreta para: {login_data.email}")
            return func.HttpResponse(
                body=json.dumps({"error": "Credenciais inválidas"}),
                status_code=401,
                mimetype="application/json"
            )
        
        # Verifica se usuário está ativo
        if not user.is_active:
            logging.warning(f"❌ Login falhou - usuário inativo: {login_data.email}")
            return func.HttpResponse(
                body=json.dumps({"error": "Conta inativa. Entre em contato com o suporte."}),
                status_code=403,
                mimetype="application/json"
            )
        
        # Atualiza último login
        user.update_last_login()
        db.commit()
        
        # Cria tokens
        access_token = create_access_token(
            user_id=user.id,
            role=user.role.value,
            email=user.email
        )
        
        refresh_token = create_refresh_token(
            user_id=user.id,
            role=user.role.value,
            email=user.email
        )
        
        # Prepara response
        response = schemas.LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user.to_dict(include_sensitive=False)
        )
        
        logging.info(f"✅ Login bem-sucedido: {user.email} ({user.role.value})")
        
        return func.HttpResponse(
            body=response.model_dump_json(),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"❌ Erro no login: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"error": "Erro interno no servidor"}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


@app.route(route="auth/refresh", methods=["POST"])
def refresh_token_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """
    Endpoint para refresh de token - gera novo access_token usando refresh_token válido
    
    Request Body:
    {
        "refresh_token": "eyJ..."
    }
    
    Response:
    {
        "access_token": "eyJ...",
        "token_type": "Bearer",
        "expires_in": 1800
    }
    """
    logging.info("🔄 Token refresh request recebido")
    
    try:
        req_body = req.get_json()
        refresh_data = schemas.RefreshTokenRequest(**req_body)
    except ValidationError as e:
        return func.HttpResponse(
            body=json.dumps({"error": "Dados inválidos", "details": e.errors()}),
            status_code=400,
            mimetype="application/json"
        )
    except ValueError:
        return func.HttpResponse(
            body=json.dumps({"error": "JSON inválido"}),
            status_code=400,
            mimetype="application/json"
        )
    
    try:
        # Valida refresh token
        payload = verify_token(refresh_data.refresh_token)
        
        # Verifica se é refresh token
        if payload.get("type") != "refresh":
            return func.HttpResponse(
                body=json.dumps({"error": "Token inválido - não é refresh token"}),
                status_code=401,
                mimetype="application/json"
            )
        
        # Cria novo access token
        new_access_token = create_access_token(
            user_id=payload["user_id"],
            role=payload["role"],
            email=payload["email"]
        )
        
        logging.info(f"✅ Token refreshed para user_id: {payload['user_id']}")
        
        return func.HttpResponse(
            body=json.dumps({
                "access_token": new_access_token,
                "token_type": "Bearer",
                "expires_in": 1800
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except ValueError as e:
        logging.warning(f"❌ Refresh token inválido: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=401,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"❌ Erro no refresh: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"error": "Erro interno no servidor"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="auth/me", methods=["GET"])
@require_auth
def get_current_user(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retorna dados do usuário autenticado
    
    Headers:
    Authorization: Bearer <access_token>
    
    Response:
    {
        "id": 1,
        "name": "João Silva",
        "email": "joao@example.com",
        "role": "TOPOGRAFO",
        ...
    }
    """
    logging.info(f"👤 Get current user - user_id: {req.user_id}")
    
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.id == req.user_id).first()
        
        if not user:
            return func.HttpResponse(
                body=json.dumps({"error": "Usuário não encontrado"}),
                status_code=404,
                mimetype="application/json"
            )
        
        user_data = schemas.UserResponse.model_validate(user)
        
        return func.HttpResponse(
            body=user_data.model_dump_json(),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"❌ Erro ao buscar usuário: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"error": "Erro interno no servidor"}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


@app.route(route="auth/register", methods=["POST"])
def register_user(req: func.HttpRequest) -> func.HttpResponse:
    """
    Registro de novo usuário
    
    Request Body:
    {
        "name": "João Silva",
        "email": "joao@example.com",
        "password": "senha123",
        "role": "CLIENTE",
        "telefone": "(11) 98765-4321",
        "cpf_cnpj": "123.456.789-00"
    }
    
    Response:
    {
        "id": 1,
        "name": "João Silva",
        "email": "joao@example.com",
        "role": "CLIENTE",
        ...
    }
    """
    logging.info("📝 Register request recebido")
    
    try:
        req_body = req.get_json()
        user_data = schemas.UserCreate(**req_body)
    except ValidationError as e:
        return func.HttpResponse(
            body=json.dumps({"error": "Dados inválidos", "details": e.errors()}),
            status_code=400,
            mimetype="application/json"
        )
    except ValueError:
        return func.HttpResponse(
            body=json.dumps({"error": "JSON inválido"}),
            status_code=400,
            mimetype="application/json"
        )
    
    db = SessionLocal()
    try:
        # Verifica se email já existe
        existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if existing_user:
            logging.warning(f"❌ Email já cadastrado: {user_data.email}")
            return func.HttpResponse(
                body=json.dumps({"error": "Email já cadastrado"}),
                status_code=409,
                mimetype="application/json"
            )
        
        # Cria novo usuário
        new_user = models.User(
            name=user_data.name,
            email=user_data.email,
            role=user_data.role,
            telefone=user_data.telefone,
            cpf_cnpj=user_data.cpf_cnpj,
            is_active=True,
            email_verified=False
        )
        new_user.set_password(user_data.password)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        user_response = schemas.UserResponse.model_validate(new_user)
        
        logging.info(f"✅ Usuário registrado: {new_user.email} ({new_user.role.value})")
        
        return func.HttpResponse(
            body=user_response.model_dump_json(),
            status_code=201,
            mimetype="application/json"
        )
        
    except IntegrityError as e:
        db.rollback()
        logging.error(f"❌ Erro de integridade: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"error": "Email já cadastrado"}),
            status_code=409,
            mimetype="application/json"
        )
    except Exception as e:
        db.rollback()
        logging.error(f"❌ Erro no registro: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"error": "Erro interno no servidor"}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


# ==================== ORIGINAL ENDPOINTS ====================

@app.route(route="lotes", methods=["POST"])
@require_auth
@require_role("TOPOGRAFO", "ADMIN")
def create_lote(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processando criacao de lote.")
    try:
        req_body = req.get_json()
        lote_data = schemas.LoteCreate(**req_body)
    except ValidationError as e:
        return func.HttpResponse(body=json.dumps({"error": "Dados invalidos", "details": e.errors()}), status_code=400, mimetype="application/json")
    except ValueError:
        return func.HttpResponse(body=json.dumps({"error": "JSON invalido"}), status_code=400, mimetype="application/json")

    db = SessionLocal()
    try:
        new_lote = logic_services.create_lote_logic(lote_data, db)
        response_data = schemas.LoteResponse.from_orm(new_lote).dict()
        response_data["criado_em"] = str(response_data["criado_em"])
        return func.HttpResponse(body=json.dumps(response_data), status_code=201, mimetype="application/json")
    except ValueError as ve:
        return func.HttpResponse(body=json.dumps({"detail": str(ve)}), status_code=400, mimetype="application/json")
    except Exception as e:
        logging.error(f"Erro interno: {e}")
        return func.HttpResponse(body=json.dumps({"error": "Erro interno"}), status_code=500, mimetype="application/json")
    finally:
        db.close()

@app.route(route="projetos", methods=["POST"])
@require_auth
@require_role("TOPOGRAFO", "ADMIN")
def create_projeto(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processando criacao de Projeto.")
    try:
        req_body = req.get_json()
        proj_data = schemas.ProjetoCreate(**req_body)
    except ValidationError as e:
        return func.HttpResponse(body=json.dumps({"error": "Dados invalidos", "details": e.errors()}), status_code=400, mimetype="application/json")
    except ValueError:
        return func.HttpResponse(body=json.dumps({"error": "JSON invalido"}), status_code=400, mimetype="application/json")

    db = SessionLocal()
    try:
        new_proj = logic_services.create_projeto_logic(proj_data, db)
        response_data = schemas.ProjetoResponse.from_orm(new_proj).dict()
        response_data["criado_em"] = str(response_data["criado_em"])
        return func.HttpResponse(body=json.dumps(response_data), status_code=201, mimetype="application/json")
    except ValueError as ve:
        return func.HttpResponse(body=json.dumps({"detail": str(ve)}), status_code=400, mimetype="application/json")
    except Exception as e:
        logging.error(f"Erro interno: {e}")
        return func.HttpResponse(body=json.dumps({"error": "Erro interno"}), status_code=500, mimetype="application/json")
    finally:
        db.close()

@app.route(route="projetos", methods=["GET"])
@require_auth
def list_projetos(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Listando projetos.")
    db = SessionLocal()
    try:
        projs = db.query(models.Projeto).all()
        results = []
        for p in projs:
            p_res = schemas.ProjetoResponse.from_orm(p).dict()
            if p_res["criado_em"]:
                p_res["criado_em"] = p_res["criado_em"].isoformat()
            results.append(p_res)
        
        return func.HttpResponse(body=json.dumps(results), status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Erro ao listar projetos: {e}")
        return func.HttpResponse(body=json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")
    finally:
        db.close()

@require_auth
@app.route(route="lotes", methods=["GET"])
def list_lotes(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Listando lotes.")
    projeto_id = req.params.get("projeto_id")
    
    db = SessionLocal()
    try:
        query = db.query(models.Lote)
        if projeto_id:
            query = query.filter(models.Lote.projeto_id == projeto_id)
        
        lotes = query.all()
        results = []
        for l in lotes:
            l_res = schemas.LoteResponse.from_orm(l).dict()
            if l_res["criado_em"]:
                l_res["criado_em"] = l_res["criado_em"].isoformat()
            if l_res["area_ha"] is not None:
                l_res["area_ha"] = float(l_res["area_ha"])
            results.append(l_res)
            
        return func.HttpResponse(body=json.dumps(results), status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Erro ao listar lotes: {e}")
        return func.HttpResponse(body=json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")
    finally:
        db.close()


# ==================== ENDPOINTS DE ASSINATURAS (PAY AS YOU GO) ====================

@app.route(route="planos", methods=["GET"])
def list_planos(req: func.HttpRequest) -> func.HttpResponse:
    """
    Lista todos os planos de pagamento disponíveis (endpoint público)
    
    GET /api/planos
    """
    logging.info("Listando planos de pagamento")
    db = SessionLocal()
    try:
        planos = logic_services.listar_planos_ativos(db)
        results = []
        
        for plano in planos:
            plano_dict = schemas.PlanoResponse.from_orm(plano).dict()
            if plano_dict.get("criado_em"):
                plano_dict["criado_em"] = plano_dict["criado_em"].isoformat()
            if plano_dict.get("preco_mensal"):
                plano_dict["preco_mensal"] = float(plano_dict["preco_mensal"])
            results.append(plano_dict)
        
        return func.HttpResponse(
            body=json.dumps(results),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Erro ao listar planos: {e}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


@app.route(route="assinaturas", methods=["POST"])
@require_auth
def create_assinatura(req: func.HttpRequest) -> func.HttpResponse:
    """
    Cria uma nova assinatura (usa user_id do token JWT)
    
    POST /api/assinaturas
    Body: {
        "plano_id": 2,
        "metodo_pagamento": "PIX"
    }
    """
    logging.info("Criando nova assinatura")
    
    try:
        req_body = req.get_json()
        assinatura_data = schemas.AssinaturaCreate(**req_body)
    except ValidationError as e:
        return func.HttpResponse(
            body=json.dumps({"error": "Dados inválidos", "details": e.errors()}),
            status_code=400,
            mimetype="application/json"
        )
    except ValueError:
        return func.HttpResponse(
            body=json.dumps({"error": "JSON inválido"}),
            status_code=400,
            mimetype="application/json"
        )
    
    db = SessionLocal()
    try:
        nova_assinatura = logic_services.criar_assinatura_logic(
            usuario_id=req.user_id,  # Usa user_id do token JWT
            plano_id=assinatura_data.plano_id,
            metodo_pagamento=assinatura_data.metodo_pagamento or "PIX",
            db=db
        )
        
        response_data = schemas.AssinaturaResponse.from_orm(nova_assinatura).dict()
        
        # Formatar datas
        for field in ["inicio_em", "expira_em", "proximo_pagamento"]:
            if response_data.get(field):
                response_data[field] = response_data[field].isoformat()
        
        return func.HttpResponse(
            body=json.dumps(response_data),
            status_code=201,
            mimetype="application/json"
        )
    except ValueError as ve:
        return func.HttpResponse(
            body=json.dumps({"error": str(ve)}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Erro ao criar assinatura: {e}")
        return func.HttpResponse(
            body=json.dumps({"error": "Erro interno"}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


@app.route(route="assinaturas/current", methods=["GET"])
@require_auth
def get_assinatura_atual(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retorna a assinatura atual do usuário autenticado
    
    GET /api/assinaturas/current
    """
    logging.info(f"Consultando assinatura atual - user_id: {req.user_id}")
    
    usuario_id = req.user_id  # Pega do token JWT
    
    db = SessionLocal()
    try:
        assinatura = logic_services.obter_assinatura_atual(int(usuario_id), db)
        
        if not assinatura:
            return func.HttpResponse(
                body=json.dumps({"message": "Nenhuma assinatura ativa encontrada"}),
                status_code=404,
                mimetype="application/json"
            )
        
        # Construir resposta com detalhes do plano
        response_data = {
            "id": assinatura.id,
            "usuario_id": assinatura.usuario_id,
            "status": assinatura.status.value,
            "inicio_em": assinatura.inicio_em.isoformat() if assinatura.inicio_em else None,
            "expira_em": assinatura.expira_em.isoformat() if assinatura.expira_em else None,
            "proximo_pagamento": assinatura.proximo_pagamento.isoformat() if assinatura.proximo_pagamento else None,
            "plano": {
                "id": assinatura.plano.id,
                "nome": assinatura.plano.nome,
                "preco_mensal": float(assinatura.plano.preco_mensal),
                "max_projetos": assinatura.plano.max_projetos,
                "max_lotes_por_projeto": assinatura.plano.max_lotes_por_projeto,
                "storage_mb": assinatura.plano.storage_mb,
            }
        }
        
        # Calcular dias restantes
        if assinatura.expira_em:
            from datetime import datetime
            dias_restantes = (assinatura.expira_em - datetime.utcnow()).days
            response_data["dias_restantes"] = max(0, dias_restantes)
        
        return func.HttpResponse(
            body=json.dumps(response_data),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Erro ao consultar assinatura: {e}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


@app.route(route="assinaturas/{id}/cancelar", methods=["POST"])
def cancelar_assinatura(req: func.HttpRequest) -> func.HttpResponse:
    """
    Cancela uma assinatura
    
    POST /api/assinaturas/{id}/cancelar
    """
    assinatura_id = req.route_params.get("id")
    logging.info(f"Cancelando assinatura {assinatura_id}")
    
    if not assinatura_id:
        return func.HttpResponse(
            body=json.dumps({"error": "ID da assinatura é obrigatório"}),
            status_code=400,
            mimetype="application/json"
        )
    
    db = SessionLocal()
    try:
        assinatura = logic_services.cancelar_assinatura_logic(int(assinatura_id), db)
        
        response_data = {
            "message": "Assinatura cancelada com sucesso",
            "assinatura_id": assinatura.id,
            "expira_em": assinatura.expira_em.isoformat() if assinatura.expira_em else None,
            "status": assinatura.status.value
        }
        
        return func.HttpResponse(
            body=json.dumps(response_data),
            status_code=200,
            mimetype="application/json"
        )
    except ValueError as ve:
        return func.HttpResponse(
            body=json.dumps({"error": str(ve)}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Erro ao cancelar assinatura: {e}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


@app.route(route="assinaturas/{id}/alterar-plano", methods=["POST"])
def alterar_plano_assinatura(req: func.HttpRequest) -> func.HttpResponse:
    """
    Altera o plano de uma assinatura (upgrade/downgrade)
    
    POST /api/assinaturas/{id}/alterar-plano
    Body: {"novo_plano_id": 3}
    """
    assinatura_id = req.route_params.get("id")
    logging.info(f"Alterando plano da assinatura {assinatura_id}")
    
    if not assinatura_id:
        return func.HttpResponse(
            body=json.dumps({"error": "ID da assinatura é obrigatório"}),
            status_code=400,
            mimetype="application/json"
        )
    
    try:
        req_body = req.get_json()
        novo_plano_id = req_body.get("novo_plano_id")
        
        if not novo_plano_id:
            return func.HttpResponse(
                body=json.dumps({"error": "novo_plano_id é obrigatório"}),
                status_code=400,
                mimetype="application/json"
            )
    except ValueError:
        return func.HttpResponse(
            body=json.dumps({"error": "JSON inválido"}),
            status_code=400,
            mimetype="application/json"
        )
    
    db = SessionLocal()
    try:
        assinatura = logic_services.alterar_plano_logic(
            int(assinatura_id),
            int(novo_plano_id),
            db
        )
        
        response_data = {
            "message": "Plano alterado com sucesso",
            "assinatura_id": assinatura.id,
            "novo_plano": {
                "id": assinatura.plano.id,
                "nome": assinatura.plano.nome,
                "preco_mensal": float(assinatura.plano.preco_mensal)
            }
        }
        
        return func.HttpResponse(
            body=json.dumps(response_data),
            status_code=200,
            mimetype="application/json"
        )
    except ValueError as ve:
        return func.HttpResponse(
            body=json.dumps({"error": str(ve)}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Erro ao alterar plano: {e}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


@app.route(route="assinaturas/{id}/renovar", methods=["POST"])
def renovar_assinatura(req: func.HttpRequest) -> func.HttpResponse:
    """
    Renova uma assinatura (chamado via webhook do gateway de pagamento)
    
    POST /api/assinaturas/{id}/renovar
    Body: {"gateway_payment_id": "pay_xyz123"}
    """
    assinatura_id = req.route_params.get("id")
    logging.info(f"Renovando assinatura {assinatura_id}")
    
    if not assinatura_id:
        return func.HttpResponse(
            body=json.dumps({"error": "ID da assinatura é obrigatório"}),
            status_code=400,
            mimetype="application/json"
        )
    
    try:
        req_body = req.get_json()
        gateway_payment_id = req_body.get("gateway_payment_id", "")
    except ValueError:
        return func.HttpResponse(
            body=json.dumps({"error": "JSON inválido"}),
            status_code=400,
            mimetype="application/json"
        )
    
    db = SessionLocal()
    try:
        assinatura = logic_services.renovar_assinatura_logic(
            int(assinatura_id),
            gateway_payment_id,
            db
        )
        
        response_data = {
            "message": "Assinatura renovada com sucesso",
            "assinatura_id": assinatura.id,
            "expira_em": assinatura.expira_em.isoformat() if assinatura.expira_em else None,
            "proximo_pagamento": assinatura.proximo_pagamento.isoformat() if assinatura.proximo_pagamento else None
        }
        
        return func.HttpResponse(
            body=json.dumps(response_data),
            status_code=200,
            mimetype="application/json"
        )
    except ValueError as ve:
        return func.HttpResponse(
            body=json.dumps({"error": str(ve)}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Erro ao renovar assinatura: {e}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


# ==================== AI / OPENROUTER ENDPOINTS ====================

@app.route(route="ai/chat", methods=["POST"])
@require_auth
def ai_chat(req: func.HttpRequest) -> func.HttpResponse:
    """
    Chat endpoint using OpenRouter Jamba model
    """
    logging.info(f"🤖 AI Chat request from user {req.user_id}")
    
    try:
        req_body = req.get_json()
        messages = req_body.get("messages")
        if not messages or not isinstance(messages, list):
            return func.HttpResponse(
                json.dumps({"error": "messages array is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        model = req_body.get("model", "ai21/jamba-large-1.7")
        temperature = float(req_body.get("temperature", 0.7))
        max_tokens = int(req_body.get("max_tokens", 4096))
        
        if not 0 <= temperature <= 2.0:
            return func.HttpResponse(
                json.dumps({"error": "temperature must be between 0 and 2.0"}),
                status_code=400,
                mimetype="application/json"
            )
        
        client = get_openrouter_client()
        response = client.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False
        )
        
        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype="application/json"
        )
        
    except ValueError as e:
        status_code, error_body = handle_openrouter_error(e)
        return func.HttpResponse(
            json.dumps(error_body),
            status_code=status_code,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"AI chat error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="ai/analyze-topography", methods=["POST"])
@require_auth
def ai_analyze_topography(req: func.HttpRequest) -> func.HttpResponse:
    """
    Analyze topography data using AI
    """
    logging.info(f"📍 Topography analysis request from user {req.user_id}")
    
    try:
        req_body = req.get_json()
        prompt = req_body.get("prompt")
        if not prompt:
            return func.HttpResponse(
                json.dumps({"error": "prompt is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        context = req_body.get("context")
        client = get_openrouter_client()
        analysis = client.analyze_topography(prompt, context)
        
        return func.HttpResponse(
            json.dumps({"analysis": analysis}),
            status_code=200,
            mimetype="application/json"
        )
        
    except ValueError as e:
        status_code, error_body = handle_openrouter_error(e)
        return func.HttpResponse(
            json.dumps(error_body),
            status_code=status_code,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Topography analysis error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="ai/generate-report", methods=["POST"])
@require_auth
def ai_generate_report(req: func.HttpRequest) -> func.HttpResponse:
    """
    Generate formatted report from topography data
    """
    logging.info(f"📊 Report generation request from user {req.user_id}")
    
    try:
        req_body = req.get_json()
        data = req_body.get("data")
        if not data or not isinstance(data, dict):
            return func.HttpResponse(
                json.dumps({"error": "data object is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        client = get_openrouter_client()
        report = client.generate_report(data)
        
        return func.HttpResponse(
            json.dumps({"report": report}),
            status_code=200,
            mimetype="application/json"
        )
        
    except ValueError as e:
        status_code, error_body = handle_openrouter_error(e)
        return func.HttpResponse(
            json.dumps(error_body),
            status_code=status_code,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Report generation error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="ai/validate-geometry", methods=["POST"])
@require_auth
def ai_validate_geometry(req: func.HttpRequest) -> func.HttpResponse:
    """
    Validate geometry description using AI
    """
    logging.info(f"✓ Geometry validation request from user {req.user_id}")
    
    try:
        req_body = req.get_json()
        description = req_body.get("description")
        if not description:
            return func.HttpResponse(
                json.dumps({"error": "description is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        client = get_openrouter_client()
        validation = client.validate_geometry_description(description)
        
        return func.HttpResponse(
            json.dumps(validation),
            status_code=200,
            mimetype="application/json"
        )
        
    except ValueError as e:
        status_code, error_body = handle_openrouter_error(e)
        return func.HttpResponse(
            json.dumps(error_body),
            status_code=status_code,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Geometry validation error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )


# ==================== GOVERNMENT DATA ENDPOINTS ====================

@app.route(route="governo/areas", methods=["GET"])
def get_government_areas(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retorna áreas governamentais registradas (SIGEF, FUNAI, ICMBio)
    Endpoint público para carregar dados de sobreposição
    
    Response:
    [
        {
            "tipo": "SIGEF",
            "nome": "Fazenda Santa Maria - Matrícula 12345",
            "coords": [[-47.89, -15.78], [-47.88, -15.78], ...]
        },
        ...
    ]
    """
    logging.info("🗺️ Carregando áreas governamentais")
    
    db = SessionLocal()
    
    try:
        # TODO: Integrar com APIs oficiais (SIGEF, FUNAI, ICMBio)
        # Por enquanto, retornamos áreas próximas a Brasília como exemplo
        
        areas = [
            {
                "tipo": "SIGEF",
                "nome": "Fazenda Santa Maria - Matrícula 12345",
                "coords": [
                    [-47.89, -15.78], [-47.88, -15.78], 
                    [-47.88, -15.79], [-47.89, -15.79], 
                    [-47.89, -15.78]
                ]
            },
            {
                "tipo": "FUNAI",
                "nome": "Terra Indígena Santuário dos Pajés",
                "coords": [
                    [-47.87, -15.80], [-47.86, -15.80], 
                    [-47.86, -15.81], [-47.87, -15.81], 
                    [-47.87, -15.80]
                ]
            },
            {
                "tipo": "ICMBio",
                "nome": "Área de Preservação Permanente - Rio Descoberto",
                "coords": [
                    [-47.92, -15.76], [-47.91, -15.76], 
                    [-47.91, -15.77], [-47.92, -15.77], 
                    [-47.92, -15.76]
                ]
            }
        ]
        
        return func.HttpResponse(
            json.dumps(areas),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Erro ao carregar áreas governamentais: {e}")
        return func.HttpResponse(
            json.dumps({"error": "Erro interno ao carregar dados"}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


# ==================== WMS LAYERS ENDPOINTS ====================

@app.route(route="wms-layers", methods=["POST"])
def create_wms_layer(req: func.HttpRequest) -> func.HttpResponse:
    """Cria uma nova camada WMS para visualização"""
    logging.info("🗺️ Criando camada WMS")
    
    db = SessionLocal()
    try:
        req_body = req.get_json()
        
        if not req_body.get("projeto_id") or not req_body.get("name") or not req_body.get("url"):
            return func.HttpResponse(
                body=json.dumps({"error": "Campos obrigatórios: projeto_id, name, url"}),
                status_code=400,
                mimetype="application/json"
            )
        
        new_layer = models.WMSLayer(
            projeto_id=req_body["projeto_id"],
            name=req_body["name"],
            url=req_body["url"],
            visible=req_body.get("visible", True),
            opacity=req_body.get("opacity", 1.0)
        )
        
        db.add(new_layer)
        db.commit()
        db.refresh(new_layer)
        
        return func.HttpResponse(
            body=json.dumps({
                "id": new_layer.id,
                "projeto_id": new_layer.projeto_id,
                "name": new_layer.name,
                "url": new_layer.url,
                "visible": new_layer.visible,
                "opacity": float(new_layer.opacity),
                "criado_em": new_layer.criado_em.isoformat()
            }),
            status_code=201,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"❌ Erro ao criar WMS layer: {e}")
        db.rollback()
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


@app.route(route="wms-layers", methods=["GET"])
def list_wms_layers(req: func.HttpRequest) -> func.HttpResponse:
    """Lista camadas WMS de um projeto"""
    logging.info("🗺️ Listando camadas WMS")
    
    projeto_id = req.params.get("projeto_id")
    if not projeto_id:
        return func.HttpResponse(
            body=json.dumps({"error": "Query param 'projeto_id' obrigatório"}),
            status_code=400,
            mimetype="application/json"
        )
    
    db = SessionLocal()
    try:
        layers = db.query(models.WMSLayer).filter(
            models.WMSLayer.projeto_id == int(projeto_id)
        ).all()
        
        layers_data = [{
            "id": layer.id,
            "projeto_id": layer.projeto_id,
            "name": layer.name,
            "url": layer.url,
            "visible": layer.visible,
            "opacity": float(layer.opacity)
        } for layer in layers]
        
        return func.HttpResponse(
            body=json.dumps(layers_data),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"❌ Erro ao listar WMS layers: {e}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


@app.route(route="wms-layers/{id}", methods=["PATCH"])
def update_wms_layer(req: func.HttpRequest) -> func.HttpResponse:
    """Atualiza camada WMS"""
    layer_id = req.route_params.get("id")
    logging.info(f"🗺️ Atualizando WMS layer {layer_id}")
    
    db = SessionLocal()
    try:
        req_body = req.get_json()
        layer = db.query(models.WMSLayer).filter(models.WMSLayer.id == int(layer_id)).first()
        
        if not layer:
            return func.HttpResponse(
                body=json.dumps({"error": "Camada WMS não encontrada"}),
                status_code=404,
                mimetype="application/json"
            )
        
        if "visible" in req_body:
            layer.visible = req_body["visible"]
        if "opacity" in req_body:
            layer.opacity = req_body["opacity"]
        
        db.commit()
        db.refresh(layer)
        
        return func.HttpResponse(
            body=json.dumps({"id": layer.id, "visible": layer.visible, "opacity": float(layer.opacity)}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"❌ Erro ao atualizar WMS layer: {e}")
        db.rollback()
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


@app.route(route="wms-layers/{id}", methods=["DELETE"])
def delete_wms_layer(req: func.HttpRequest) -> func.HttpResponse:
    """Deleta camada WMS"""
    layer_id = req.route_params.get("id")
    logging.info(f"🗺️ Deletando WMS layer {layer_id}")
    
    db = SessionLocal()
    try:
        layer = db.query(models.WMSLayer).filter(models.WMSLayer.id == int(layer_id)).first()
        
        if not layer:
            return func.HttpResponse(
                body=json.dumps({"error": "Camada WMS não encontrada"}),
                status_code=404,
                mimetype="application/json"
            )
        
        db.delete(layer)
        db.commit()
        
        return func.HttpResponse(
            body=json.dumps({"message": "Camada WMS deletada com sucesso"}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"❌ Erro ao deletar WMS layer: {e}")
        db.rollback()
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


# ==================== CHAT ENDPOINTS ====================

@app.route(route="chat/messages", methods=["POST"])
def send_chat_message(req: func.HttpRequest) -> func.HttpResponse:
    """Envia mensagem no chat"""
    logging.info("💬 Enviando mensagem")
    
    db = SessionLocal()
    try:
        req_body = req.get_json()
        required = ["projeto_id", "sender_id", "sender_role", "message"]
        if not all(field in req_body for field in required):
            return func.HttpResponse(
                body=json.dumps({"error": f"Campos obrigatórios: {', '.join(required)}"}),
                status_code=400,
                mimetype="application/json"
            )
        
        new_message = models.ChatMessage(
            projeto_id=req_body["projeto_id"],
            sender_id=req_body["sender_id"],
            sender_role=req_body["sender_role"],
            message=req_body["message"]
        )
        
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        
        return func.HttpResponse(
            body=json.dumps({
                "id": new_message.id,
                "projeto_id": new_message.projeto_id,
                "sender_id": new_message.sender_id,
                "sender_role": new_message.sender_role,
                "message": new_message.message,
                "is_read": new_message.is_read,
                "criado_em": new_message.criado_em.isoformat()
            }),
            status_code=201,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"❌ Erro ao enviar mensagem: {e}")
        db.rollback()
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


@app.route(route="chat/messages", methods=["GET"])
def get_chat_messages(req: func.HttpRequest) -> func.HttpResponse:
    """Lista mensagens do chat"""
    logging.info("💬 Listando mensagens")
    
    projeto_id = req.params.get("projeto_id")
    limit = int(req.params.get("limit", 50))
    
    if not projeto_id:
        return func.HttpResponse(
            body=json.dumps({"error": "Query param 'projeto_id' obrigatório"}),
            status_code=400,
            mimetype="application/json"
        )
    
    db = SessionLocal()
    try:
        messages = db.query(models.ChatMessage).filter(
            models.ChatMessage.projeto_id == int(projeto_id)
        ).order_by(models.ChatMessage.criado_em.desc()).limit(limit).all()
        
        messages_data = [{
            "id": msg.id,
            "sender_id": msg.sender_id,
            "sender_role": msg.sender_role,
            "message": msg.message,
            "is_read": msg.is_read,
            "criado_em": msg.criado_em.isoformat()
        } for msg in messages]
        
        messages_data.reverse()
        
        return func.HttpResponse(
            body=json.dumps(messages_data),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"❌ Erro ao listar mensagens: {e}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


# ==================== STATUS HISTORY ENDPOINT ====================

@app.route(route="lotes/{id}/status-history", methods=["GET"])
def get_status_history(req: func.HttpRequest) -> func.HttpResponse:
    """Retorna histórico de status"""
    lote_id = req.route_params.get("id")
    logging.info(f"📜 Buscando histórico do lote {lote_id}")
    
    db = SessionLocal()
    try:
        history = db.query(models.StatusHistory).filter(
            models.StatusHistory.lote_id == int(lote_id)
        ).order_by(models.StatusHistory.criado_em.asc()).all()
        
        history_data = [{
            "id": h.id,
            "status_anterior": h.status_anterior.value if h.status_anterior else None,
            "status_novo": h.status_novo.value,
            "observacao": h.observacao,
            "alterado_por": h.alterado_por,
            "criado_em": h.criado_em.isoformat()
        } for h in history]
        
        return func.HttpResponse(
            body=json.dumps(history_data),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"❌ Erro ao buscar histórico: {e}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()


# ==================== MAGIC LINK ENDPOINT ====================

@app.route(route="auth/magic-link/{token}", methods=["GET"])
def validate_magic_link(req: func.HttpRequest) -> func.HttpResponse:
    """Valida magic link"""
    token = req.route_params.get("token")
    logging.info(f"🔗 Validando magic link: {token}")
    
    db = SessionLocal()
    try:
        lote = db.query(models.Lote).filter(models.Lote.token_acesso == token).first()
        
        if not lote:
            return func.HttpResponse(
                body=json.dumps({"valid": False, "error": "Link inválido"}),
                status_code=404,
                mimetype="application/json"
            )
        
        if lote.link_expira_em and lote.link_expira_em < datetime.utcnow():
            return func.HttpResponse(
                body=json.dumps({"valid": False, "error": "Link expirado"}),
                status_code=403,
                mimetype="application/json"
            )
        
        access_token = create_access_token(user_id=lote.id, role="CLIENTE")
        
        return func.HttpResponse(
            body=json.dumps({
                "valid": True,
                "access_token": access_token,
                "token_type": "Bearer",
                "lote": {
                    "id": lote.id,
                    "projeto_id": lote.projeto_id,
                    "nome_cliente": lote.nome_cliente,
                    "email_cliente": lote.email_cliente,
                    "status": lote.status.value,
                    "area_ha": float(lote.area_ha) if lote.area_ha else None
                }
            }),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"❌ Erro ao validar magic link: {e}")
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        db.close()

