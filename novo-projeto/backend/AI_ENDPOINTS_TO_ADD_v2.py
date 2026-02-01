# ==================== NOVOS ENDPOINTS PARA ADICIONAR AO function_app.py ====================
# Cole este código no FINAL do arquivo function_app.py

# ==================== WMS LAYERS ENDPOINTS ====================

@app.route(route="wms-layers", methods=["POST"])
def create_wms_layer(req: func.HttpRequest) -> func.HttpResponse:
    """
    Cria uma nova camada WMS para visualização
    
    Request Body:
    {
        "projeto_id": 1,
        "name": "SIGEF - Goiás",
        "url": "https://sigef.incra.gov.br/wms",
        "visible": true,
        "opacity": 0.7
    }
    """
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
    """Lista camadas WMS de um projeto - Query Params: projeto_id"""
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
        
        layers_data = []
        for layer in layers:
            layers_data.append({
                "id": layer.id,
                "projeto_id": layer.projeto_id,
                "name": layer.name,
                "url": layer.url,
                "visible": layer.visible,
                "opacity": float(layer.opacity)
            })
        
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
    """Atualiza visibilidade/opacity de uma camada WMS"""
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
            body=json.dumps({
                "id": layer.id,
                "visible": layer.visible,
                "opacity": float(layer.opacity)
            }),
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
    """Deleta uma camada WMS"""
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
    """Envia mensagem no chat do projeto"""
    logging.info("💬 Enviando mensagem de chat")
    
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
    """Lista mensagens do chat (polling simples) - Query: projeto_id, limit"""
    logging.info("💬 Listando mensagens de chat")
    
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
        ).order_by(
            models.ChatMessage.criado_em.desc()
        ).limit(limit).all()
        
        messages_data = []
        for msg in messages:
            messages_data.append({
                "id": msg.id,
                "sender_id": msg.sender_id,
                "sender_role": msg.sender_role,
                "message": msg.message,
                "is_read": msg.is_read,
                "criado_em": msg.criado_em.isoformat()
            })
        
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
    """Retorna histórico de mudanças de status de um lote (Timeline)"""
    lote_id = req.route_params.get("id")
    logging.info(f"📜 Buscando histórico de status do lote {lote_id}")
    
    db = SessionLocal()
    try:
        history = db.query(models.StatusHistory).filter(
            models.StatusHistory.lote_id == int(lote_id)
        ).order_by(
            models.StatusHistory.criado_em.asc()
        ).all()
        
        history_data = []
        for h in history:
            history_data.append({
                "id": h.id,
                "status_anterior": h.status_anterior.value if h.status_anterior else None,
                "status_novo": h.status_novo.value,
                "observacao": h.observacao,
                "alterado_por": h.alterado_por,
                "criado_em": h.criado_em.isoformat()
            })
        
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
    """
    Valida magic link e retorna JWT + dados do cliente
    URL: /api/auth/magic-link/550e8400-e29b-41d4-a716-446655440000
    """
    token = req.route_params.get("token")
    logging.info(f"🔗 Validando magic link: {token}")
    
    db = SessionLocal()
    try:
        lote = db.query(models.Lote).filter(
            models.Lote.token_acesso == token
        ).first()
        
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
        
        access_token = create_access_token(
            user_id=lote.id,
            role="CLIENTE"
        )
        
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
