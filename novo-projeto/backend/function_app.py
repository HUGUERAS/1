import azure.functions as func
import logging
import json
import os
from database import SessionLocal, engine
import models
import schemas
import logic_services
from pydantic import ValidationError

# Comentado para evitar crash no startup - tabelas ja criadas via script
# models.Base.metadata.create_all(bind=engine)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="lotes", methods=["POST"])
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
    Lista todos os planos de pagamento disponíveis
    
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
def create_assinatura(req: func.HttpRequest) -> func.HttpResponse:
    """
    Cria uma nova assinatura
    
    POST /api/assinaturas
    Body: {
        "usuario_id": 123,
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
            usuario_id=assinatura_data.usuario_id,
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
def get_assinatura_atual(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retorna a assinatura atual do usuário
    
    GET /api/assinaturas/current?usuario_id=123
    """
    logging.info("Consultando assinatura atual")
    
    usuario_id = req.params.get("usuario_id")
    if not usuario_id:
        return func.HttpResponse(
            body=json.dumps({"error": "usuario_id é obrigatório"}),
            status_code=400,
            mimetype="application/json"
        )
    
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
