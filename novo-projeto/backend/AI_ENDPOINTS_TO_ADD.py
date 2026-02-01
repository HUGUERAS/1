# Adicione essas linhas ao final de novo-projeto/backend/function_app.py

# ==================== AI / OPENROUTER ENDPOINTS ====================

@app.route(route="ai/chat", methods=["POST"])
@require_auth
def ai_chat(req: func.HttpRequest) -> func.HttpResponse:
    """
    Chat endpoint using OpenRouter Jamba model
    """
    logging.info(f"AI Chat request from user {req.user_id}")
    
    try:
        req_body = req.get_json()
        messages = req_body.get("messages")
        if not messages or not isinstance(messages, list):
            return func.HttpResponse(
                json.dumps({"error": "messages array is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        model = req_body.get("model", "jamba-1.5-large")
        temperature = float(req_body.get("temperature", 0.7))
        max_tokens = int(req_body.get("max_tokens", 2048))
        
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
    logging.info(f"Topography analysis request from user {req.user_id}")
    
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
    logging.info(f"Report generation request from user {req.user_id}")
    
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
    logging.info(f"Geometry validation request from user {req.user_id}")
    
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
