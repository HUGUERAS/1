import azure.functions as func
import logging
import json
import os
import psycopg2
from datetime import datetime
import uuid
import db_setup
# from infinitepay_payment import infinitepay_bp  # TODO: Isolate InfinitePay until API key is configured

# Configuração da App Function (Python v2 Model)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Registrar blueprint do InfinitePay
# app.register_functions(infinitepay_bp)  # TODO: Enable once INFINITEPAY_API_KEY is set

# Flag global para evitar checagem repetitiva no mesmo worker
_SCHEMA_CHECKED = False

def get_db_connection():
    """Estabelece conexão com o Azure PostgreSQL"""
    global _SCHEMA_CHECKED
    try:
        # A Connection String deve estar nas Configurações da Function (App Settings)
        # Formato esperado: "dbname=... user=... password=... host=... sslmode=require"
        conn_str = os.environ.get("POSTGRES_CONNECTION_STRING")
        if not conn_str:
            raise Exception("POSTGRES_CONNECTION_STRING não definida")
        
        conn = psycopg2.connect(conn_str)
        
        # Inicializa o banco na primeira conexão deste worker
        if not _SCHEMA_CHECKED:
            db_setup.ensure_schema(conn)
            _SCHEMA_CHECKED = True
            
        return conn
    except Exception as e:
        logging.error(f"Erro de conexão com DB: {e}")
        return None

@app.route(route="rural/onboard", methods=["POST"])
def rural_onboard(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processando cadastro rural (Python).')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "Invalid JSON"}), status_code=400, mimetype="application/json")

    # Extrair dados do request
    farm_name = req_body.get('farmName')
    document = req_body.get('document')
    area = req_body.get('area')
    email = req_body.get('email')

    # Validação Básica
    if not all([farm_name, document, area, email]):
        return func.HttpResponse(
            json.dumps({"error": "Campos obrigatórios: farmName, document, area, email"}),
            status_code=400, mimetype="application/json"
        )
    
    try:
        area_float = float(area)
        if area_float <= 0:
             raise ValueError
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "A area deve ser um número positivo"}),
            status_code=400, mimetype="application/json"
        )

    conn = get_db_connection()
    if not conn:
        # Fallback se não tiver banco configurado (para testes locais sem banco)
        logging.warning("Banco não configurado, retornando mock.")
        return func.HttpResponse(
            json.dumps({
                "message": "Cadastro simulado (Banco não conectado)",
                "organizationId": f"mock-{uuid.uuid4()}",
                "status": "warning"
            }),
            status_code=201, mimetype="application/json"
        )

    try:
        cur = conn.cursor()
        
        # Gerar IDs
        user_id = str(uuid.uuid4())
        
        # Metadados em JSON
        metadados = json.dumps({
            "documento": document,
            "area_declarada_ha": area_float,
            "origem": "web_onboarding"
        })

        # Query de Inserção (SQL Seguro)
        insert_query = """
            INSERT INTO propriedades (user_id, nome_proprietario, email_proprietario, nome_imovel, tipo_imovel, metadados_rurais)
            VALUES (%s, %s, %s, %s, 'RURAL', %s)
            RETURNING id;
        """
        
        # Assumindo que o nome do proprietário é o mesmo da fazenda ou extraído (simplificação)
        # Num cenário real, pediríamos "Nome do Proprietário" separado
        cur.execute(insert_query, (user_id, farm_name, email, farm_name, metadados))
        new_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()

        return func.HttpResponse(
            json.dumps({
                "message": "Propriedade rural cadastrada com sucesso",
                "id_propriedade": new_id,
                "user_id": user_id
            }),
            status_code=201, mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Erro ao salvar no banco: {e}")
        return func.HttpResponse(
            json.dumps({"error": "Erro interno ao salvar dados"}),
            status_code=500, mimetype="application/json"
        )

@app.route(route="urban/activate", methods=["POST"])
def urban_activate(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processando ativação urbana (Python).')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "Invalid JSON"}), status_code=400, mimetype="application/json")

    cpf = req_body.get('cpf')
    birth_date = req_body.get('birthDate')
    password = req_body.get('password')

    # Validação Básica
    if not all([cpf, birth_date, password]):
        return func.HttpResponse(
            json.dumps({"error": "Campos obrigatórios: cpf, birthDate, password"}),
            status_code=400, mimetype="application/json"
        )

    # Limpeza de CPF (Apenas números)
    cpf_clean = "".join(filter(str.isdigit, str(cpf)))
    if len(cpf_clean) != 11:
         return func.HttpResponse(
            json.dumps({"error": "CPF deve ter 11 dígitos"}),
            status_code=400, mimetype="application/json"
        )

    conn = get_db_connection()
    if not conn:
        logging.warning("Banco não configurado, retornando mock urbano.")
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "userId": f"urban-mock-{uuid.uuid4()}",
                "message": "Conta urbana ativada (Simulação)"
            }),
            status_code=200, mimetype="application/json"
        )

    try:
        cur = conn.cursor()
        user_id = str(uuid.uuid4())
        
        # Metadados Urbanos
        metadados = json.dumps({
            "cpf": cpf_clean,
            "data_nascimento": birth_date,
            "origem": "web_urban_activation"
        })

        # Inserção no Banco (Tipo URBANO)
        # Nota: Normalmente salvaríamos o usuário numa tabela separada 'users' com hash de senha
        # Aqui estamos simplificando salvando direto na tabela 'propriedades' como um registro inicial
        insert_query = """
            INSERT INTO propriedades (user_id, nome_proprietario, email_proprietario, nome_imovel, tipo_imovel, metadados_urbanos)
            VALUES (%s, %s, 'N/A', 'Imóvel Urbano - Novo', 'URBANO', %s)
            RETURNING id;
        """
        
        cur.execute(insert_query, (user_id, f"CPF {cpf_clean}", metadados))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return func.HttpResponse(
            json.dumps({
                "success": True,
                "userId": user_id,
                "propriedadeId": new_id,
                "message": "Conta urbana ativada com sucesso"
            }),
            status_code=200, mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Erro ao salvar urbano: {e}")
        return func.HttpResponse(
            json.dumps({"error": "Erro ao processar ativação urbana"}),
            status_code=500, mimetype="application/json"
        )

@app.route(route="tech/login", methods=["POST"])
def tech_login(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processando login técnico (Python).')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "Invalid JSON"}), status_code=400, mimetype="application/json")

    username = req_body.get('username')
    password = req_body.get('password')

    if not username or not password:
         return func.HttpResponse(
            json.dumps({"error": "Usuário e senha necessários"}),
            status_code=400, mimetype="application/json"
        )

    # Simulação de Autenticação (Banco mockado/hardcoded por segurança inicial)
    # Num cenário real: SELECT * FROM tecnicos WHERE user = ... AND pass_hash = ...
    if username == "admin" and password == "admin123":
         return func.HttpResponse(
            json.dumps({
                "success": True,
                "sessionId": f"sess-{uuid.uuid4()}",
                "message": "Login técnico realizado",
                "role": "admin"
            }),
            status_code=200, mimetype="application/json"
        )
    
    return func.HttpResponse(
        json.dumps({"error": "Credenciais inválidas"}),
        status_code=401, mimetype="application/json"
    )

@app.route(route="login", methods=["POST"])
def login_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processando login de usuário.')

    try:
        req_body = req.get_json()
        email = req_body.get('email')
        password = req_body.get('password')
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "Corpo da requisição inválido"}), status_code=400, mimetype="application/json")

    if not email or not password:
        return func.HttpResponse(json.dumps({"error": "Email e senha são obrigatórios"}), status_code=400, mimetype="application/json")

    conn = get_db_connection()
    if not conn:
        return func.HttpResponse(json.dumps({"error": "Banco de dados indisponível"}), status_code=503, mimetype="application/json")

    try:
        with conn.cursor() as cur:
            # Query users table
            cur.execute("SELECT id, name, role, password_hash FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            
            if user:
                # user = (id, name, role, password_hash)
                stored_pass = user[3]
                
                # Comparação simples conforme solicitado (idealmente usar bcrypt)
                if password == stored_pass:
                    return func.HttpResponse(
                        json.dumps({
                            "id": str(user[0]),
                            "name": user[1],
                            "role": user[2]
                        }), status_code=200, mimetype="application/json"
                    )
            
            return func.HttpResponse(json.dumps({"error": "Credenciais inválidas"}), status_code=401, mimetype="application/json")

    except Exception as e:
        logging.error(f"Erro no login: {e}")
        return func.HttpResponse(json.dumps({"error": "Erro interno no servidor"}), status_code=500, mimetype="application/json")
    finally:
        if conn: conn.close()

@app.route(route="rural/dashboard/{user_id}", methods=["GET"])
def get_rural_dashboard(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.route_params.get('user_id')
    logging.info(f'Buscando dashboard rural para usuário {user_id}.')

    conn = get_db_connection()
    if not conn:
        return func.HttpResponse(json.dumps({"error": "Banco de dados indisponível"}), status_code=503, mimetype="application/json")

    try:
        with conn.cursor() as cur:
            # Buscar propriedade
            cur.execute("SELECT id, nome_imovel, metadados_rurais, status FROM propriedades WHERE user_id = %s LIMIT 1", (user_id,))
            prop = cur.fetchone()

            if not prop:
                return func.HttpResponse(json.dumps({"message": "Nenhuma propriedade encontrada"}), status_code=404, mimetype="application/json")

            prop_id = prop[0]
            
            # Buscar confrontantes associados à propriedade
            cur.execute("SELECT id, nome, status, contato FROM confrontantes WHERE propriedade_id = %s", (prop_id,))
            confrontantes_rows = cur.fetchall()
            
            confrontantes = []
            for row in confrontantes_rows:
                 confrontantes.append({
                     "id": row[0],
                     "nome": row[1],
                     "status": row[2],
                     "contato": row[3]
                 })

            response_data = {
                "id": prop[0],
                "nome_imovel": prop[1],
                "status": prop[3],
                "metadados": prop[2],
                "confrontantes": confrontantes
            }

            return func.HttpResponse(
                json.dumps(response_data, default=str), 
                status_code=200, mimetype="application/json"
            )

    except Exception as e:
        logging.error(f"Erro no dashboard rural: {e}")
        return func.HttpResponse(json.dumps({"error": "Erro interno no servidor"}), status_code=500, mimetype="application/json")
    finally:
        if conn: conn.close()
