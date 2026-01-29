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
