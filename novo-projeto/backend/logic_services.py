from sqlalchemy.orm import Session
from sqlalchemy import text
from shapely.geometry import Polygon
from shapely import wkt
import models
import logging

# --- CONFIGURAÇÃO DE TOLERÂNCIAS ---
TOLERANCIA_SOBREPOSICAO_GRAUS = 0.0000001 # ~1cm² no Equador
TOLERANCIA_SNAP_METROS = 0.5 # 50cm para avisar "você errou por pouco"
SRID_OFICIAL = 4674 # SIRGAS 2000

def check_overlap_warnings(wkt_geometry: str, projeto_id: int, db: Session) -> list:
    """
    Verifica se existe interseção REAL (area > 0) com SIGEF ou vizinhos.
    Retorna: list[str] de avisos (NÃO É MAIS BLOQUEANTE).
    """
    avisos = []
    
    # 1. Validação SIGEF (Dados Federais)
    stmt_sigef = text(f"""
        SELECT codigo_imovel, detentor
        FROM sigef_incra 
        WHERE ST_Intersects(geom, ST_GeomFromText(:wkt, {SRID_OFICIAL}))
        AND ST_Area(ST_Intersection(geom, ST_GeomFromText(:wkt, {SRID_OFICIAL}))) > :tol
    """)
    
    conflitos_sigef = db.execute(stmt_sigef, {"wkt": wkt_geometry, "tol": TOLERANCIA_SOBREPOSICAO_GRAUS}).fetchall()
    if conflitos_sigef:
        detalhes = ", ".join([f"{row[0]} ({row[1]})" for row in conflitos_sigef])
        avisos.append(f"ALERTA: Área sobrepõe terras certificadas (SIGEF/INCRA): {detalhes}. Avaliação do Topógrafo necessária.")

    # 2. Validação de Vizinhos do Mesmo Projeto
    if projeto_id:
        stmt_vizinhos = text(f"""
            SELECT nome_cliente
            FROM lotes
            WHERE projeto_id = :pid
            AND ST_Intersects(geom, ST_GeomFromText(:wkt, {SRID_OFICIAL}))
            AND ST_Area(ST_Intersection(geom, ST_GeomFromText(:wkt, {SRID_OFICIAL}))) > :tol
        """)
        
        conflitos_vizinhos = db.execute(stmt_vizinhos, {
            "wkt": wkt_geometry, 
            "pid": projeto_id,
            "tol": TOLERANCIA_SOBREPOSICAO_GRAUS
        }).fetchall()
        
        if conflitos_vizinhos:
            nomes = ", ".join([r[0] for r in conflitos_vizinhos if r[0]])
            avisos.append(f"ALERTA: Sobreposição detectada com lote vizinho: {nomes}. Verifique o croqui.")

    return avisos

def check_proximity(wkt_geometry: str, projeto_id: int, db: Session):
    """
    Verifica "buracos finos" (slivers) entre vizinhos.
    Se estiver muito perto mas não tocando, avisa para usar Snap.
    Retorna: list[str] de avisos.
    """
    avisos = []
    
    if not projeto_id:
        return avisos

    # Busca vizinhos que estão "quase tocando" (DWithin) mas não interceptam
    # Usamos cast para geography para ter medida em METROS
    stmt_gap = text(f"""
        SELECT nome_cliente
        FROM lotes
        WHERE projeto_id = :pid
        AND ST_DWithin(geom::geography, ST_GeomFromText(:wkt, {SRID_OFICIAL})::geography, :dist_metros)
        AND NOT ST_Intersects(geom, ST_GeomFromText(:wkt, {SRID_OFICIAL}))
    """)
    
    vizinhos_proximos = db.execute(stmt_gap, {
        "wkt": wkt_geometry, 
        "pid": projeto_id,
        "dist_metros": TOLERANCIA_SNAP_METROS
    }).fetchall()
    
    for v in vizinhos_proximos:
        nome = v[0] or "Vizinho Desconhecido"
        avisos.append(f"ALERTA: Fresta detectada entre este lote e {nome} (< 50cm). Recomendado usar ferramenta 'Snap' para fechar o perímetro.")
        
    return avisos

def create_lote_logic(lote_data, db: Session):
    # 1. Higienização da Geometria
    try:
        coords_fixed = [(p[1], p[0]) for p in lote_data.coordinates] # Inverte Lat/Lon para Lon/Lat (PostGIS)
        poly = Polygon(coords_fixed)
        if not poly.is_valid:
            poly = poly.buffer(0) # Corrige auto-interseções simples
        wkt_str = poly.wkt
    except Exception as e:
        raise ValueError(f"Geometria inválida: {str(e)}")
    
    # 2. Validação Não-Bloqueante (Apenas Warnings)
    warnings = []
    
    # Sobreposições (Agora apenas informativas)
    overlap_warnings = check_overlap_warnings(wkt_str, lote_data.projeto_id, db)
    warnings.extend(overlap_warnings)
    
    # Proximidade/Frestas
    proximity_warnings = check_proximity(wkt_str, lote_data.projeto_id, db)
    warnings.extend(proximity_warnings)
    
    # 3. Criação do Registro
    # Calcula metadados geométricos antes de salvar
    # NOTA: ST_Area(geography) retorna em m², divide por 10.000 para Hectares
    stmt_area = text(f"SELECT ST_Area(ST_GeomFromText(:wkt, {SRID_OFICIAL})::geography) / 10000.0")
    area_calc = db.execute(stmt_area, {"wkt": wkt_str}).scalar()
    
    stmt_perimetro = text(f"SELECT ST_Length(ST_GeomFromText(:wkt, {SRID_OFICIAL})::geography)")
    perimetro_calc = db.execute(stmt_perimetro, {"wkt": wkt_str}).scalar()

    db_lote = models.Lote(
        nome_cliente=lote_data.proprietario, # Mapeando proprietario -> nome_cliente
        email_cliente="pendente@email.com", # Placeholder
        matricula=lote_data.matricula,
        projeto_id=lote_data.projeto_id,
        geom=wkt_str,
        area_ha=area_calc,
        perimetro_m=perimetro_calc,
        metadata_validacao={"warnings": warnings, "validado_automaticamente": True}
    )
    
    db.add(db_lote)
    db.commit()
    db.refresh(db_lote)
    return db_lote

def create_projeto_logic(projeto_data, db: Session):
    # Projeto agora é puramente lógico, sem obrigatoriedade de geometria da Gleba Mãe
    # Mas se o usuário mandar coordenadas, salvamos como referência (opcional)
    
    wkt_mae = None
    if projeto_data.coordinates and len(projeto_data.coordinates) > 2:
        try:
            coords_fixed = [(p[1], p[0]) for p in projeto_data.coordinates]
            poly = Polygon(coords_fixed)
            if not poly.is_valid: poly = poly.buffer(0)
            wkt_mae = poly.wkt
            
            # Opcional: Validar se a Gleba Mãe inteira cai em terra indígena
            warnings_mae = check_overlap_warnings(wkt_mae, None, db)
            if warnings_mae:
                 logging.warning(f"Aviso: Gleba mãe sobrepõe área restrita: {warnings_mae}")
                 
        except Exception as e:
            logging.warning(f"Erro ao processar geometria da Gleba Mãe (ignorado): {e}")

    # Atenção: models.Projeto não tem mais `geom` ou `matricula_mae` obrigatórios
    # Se existirem no model atualizado, usamos. Se não, ignoramos.
    # No passo anterior, removemos geom_mae do create table, mas vamos checar o models.py em runtime
    # Como o models.py foi atualizado para remover geom_mae, aqui criamos apenas os dados cadastrais.
    
    db_projeto = models.Projeto(
        nome=projeto_data.nome,
        descricao=projeto_data.descricao,
        tipo=projeto_data.tipo if hasattr(projeto_data, 'tipo') else 'INDIVIDUAL',
        # matricula_mae e geom_mae foram removidos do modelo principal para simplificação
    )
    
    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    return db_projeto


# ==================== LÓGICA DE ASSINATURAS (PAY AS YOU GO) ====================

def listar_planos_ativos(db: Session):
    """
    Lista todos os planos de pagamento ativos ordenados por ordem_exibicao
    """
    return db.query(models.PlanoPagamento).filter(
        models.PlanoPagamento.ativo == True
    ).order_by(models.PlanoPagamento.ordem_exibicao).all()


def obter_plano_por_id(plano_id: int, db: Session):
    """
    Obtém um plano específico por ID
    """
    plano = db.query(models.PlanoPagamento).filter(
        models.PlanoPagamento.id == plano_id,
        models.PlanoPagamento.ativo == True
    ).first()
    
    if not plano:
        raise ValueError(f"Plano {plano_id} não encontrado ou inativo")
    
    return plano


def criar_assinatura_logic(usuario_id: int, plano_id: int, metodo_pagamento: str, db: Session):
    """
    Cria uma nova assinatura para um usuário
    
    Args:
        usuario_id: ID do usuário (topógrafo/cliente)
        plano_id: ID do plano escolhido
        metodo_pagamento: Método de pagamento (PIX, CARTAO, BOLETO)
        db: Sessão do banco de dados
    
    Returns:
        Assinatura criada
    
    Raises:
        ValueError: Se plano não existe ou usuário já tem assinatura ativa
    """
    from datetime import datetime, timedelta
    
    # Verificar se plano existe
    plano = obter_plano_por_id(plano_id, db)
    
    # Verificar se usuário já tem assinatura ativa
    assinatura_existente = db.query(models.Assinatura).filter(
        models.Assinatura.usuario_id == usuario_id,
        models.Assinatura.status.in_(['ATIVA', 'TRIAL', 'PENDENTE'])
    ).first()
    
    if assinatura_existente:
        raise ValueError(f"Usuário já possui assinatura ativa (ID: {assinatura_existente.id})")
    
    # Criar nova assinatura
    nova_assinatura = models.Assinatura(
        usuario_id=usuario_id,
        plano_id=plano_id,
        status=models.StatusAssinaturaEnum.PENDENTE if plano.preco_mensal > 0 else models.StatusAssinaturaEnum.TRIAL,
        metodo_pagamento=metodo_pagamento,
        inicio_em=datetime.utcnow(),
        expira_em=datetime.utcnow() + timedelta(days=30) if plano.preco_mensal == 0 else None,
        proximo_pagamento=datetime.utcnow() if plano.preco_mensal > 0 else None,
        metadata={"criacao": "auto", "plano_nome": plano.nome}
    )
    
    db.add(nova_assinatura)
    db.commit()
    db.refresh(nova_assinatura)
    
    # Registrar no histórico
    registrar_evento_historico(
        assinatura_id=nova_assinatura.id,
        acao="CRIADA",
        plano_novo_id=plano_id,
        detalhes={"metodo_pagamento": metodo_pagamento},
        criado_por=f"usuario_{usuario_id}",
        db=db
    )
    
    return nova_assinatura


def obter_assinatura_atual(usuario_id: int, db: Session):
    """
    Obtém a assinatura ativa/trial atual do usuário
    
    Returns:
        Assinatura com plano, ou None se não houver
    """
    from datetime import datetime
    
    assinatura = db.query(models.Assinatura).filter(
        models.Assinatura.usuario_id == usuario_id,
        models.Assinatura.status.in_(['ATIVA', 'TRIAL'])
    ).order_by(models.Assinatura.criado_em.desc()).first()
    
    return assinatura


def cancelar_assinatura_logic(assinatura_id: int, db: Session):
    """
    Cancela uma assinatura. O acesso permanece até a data de expiração.
    
    Args:
        assinatura_id: ID da assinatura a cancelar
        db: Sessão do banco de dados
    
    Returns:
        Assinatura cancelada
    """
    from datetime import datetime
    
    assinatura = db.query(models.Assinatura).filter(
        models.Assinatura.id == assinatura_id
    ).first()
    
    if not assinatura:
        raise ValueError(f"Assinatura {assinatura_id} não encontrada")
    
    if assinatura.status == models.StatusAssinaturaEnum.CANCELADA:
        raise ValueError("Assinatura já está cancelada")
    
    plano_anterior_id = assinatura.plano_id
    
    # Atualizar status
    assinatura.status = models.StatusAssinaturaEnum.CANCELADA
    assinatura.cancelada_em = datetime.utcnow()
    assinatura.proximo_pagamento = None  # Cancelar cobranças futuras
    
    db.commit()
    db.refresh(assinatura)
    
    # Registrar no histórico
    registrar_evento_historico(
        assinatura_id=assinatura.id,
        acao="CANCELADA",
        plano_anterior_id=plano_anterior_id,
        detalhes={"cancelamento_em": datetime.utcnow().isoformat()},
        criado_por=f"usuario_{assinatura.usuario_id}",
        db=db
    )
    
    return assinatura


def alterar_plano_logic(assinatura_id: int, novo_plano_id: int, db: Session):
    """
    Altera o plano de uma assinatura (upgrade ou downgrade)
    
    Args:
        assinatura_id: ID da assinatura
        novo_plano_id: ID do novo plano
        db: Sessão do banco de dados
    
    Returns:
        Assinatura atualizada
    """
    from datetime import datetime
    
    assinatura = db.query(models.Assinatura).filter(
        models.Assinatura.id == assinatura_id
    ).first()
    
    if not assinatura:
        raise ValueError(f"Assinatura {assinatura_id} não encontrada")
    
    if assinatura.status not in [models.StatusAssinaturaEnum.ATIVA, models.StatusAssinaturaEnum.TRIAL]:
        raise ValueError("Só é possível alterar plano de assinaturas ativas ou em trial")
    
    novo_plano = obter_plano_por_id(novo_plano_id, db)
    plano_anterior = assinatura.plano
    
    if plano_anterior.id == novo_plano.id:
        raise ValueError("O novo plano é igual ao atual")
    
    # Determinar se é upgrade ou downgrade
    acao = "UPGRADE" if novo_plano.preco_mensal > plano_anterior.preco_mensal else "DOWNGRADE"
    
    # Atualizar assinatura
    plano_anterior_id = assinatura.plano_id
    assinatura.plano_id = novo_plano_id
    
    # Atualizar metadata
    if not assinatura.metadata:
        assinatura.metadata = {}
    if "alteracoes_plano" not in assinatura.metadata:
        assinatura.metadata["alteracoes_plano"] = []
    
    assinatura.metadata["alteracoes_plano"].append({
        "de": plano_anterior.nome,
        "para": novo_plano.nome,
        "acao": acao,
        "data": datetime.utcnow().isoformat()
    })
    
    db.commit()
    db.refresh(assinatura)
    
    # Registrar no histórico
    registrar_evento_historico(
        assinatura_id=assinatura.id,
        acao=acao,
        plano_anterior_id=plano_anterior_id,
        plano_novo_id=novo_plano_id,
        detalhes={
            "plano_anterior": plano_anterior.nome,
            "plano_novo": novo_plano.nome,
            "diferenca_preco": float(novo_plano.preco_mensal - plano_anterior.preco_mensal)
        },
        criado_por=f"usuario_{assinatura.usuario_id}",
        db=db
    )
    
    return assinatura


def renovar_assinatura_logic(assinatura_id: int, gateway_payment_id: str, db: Session):
    """
    Renova uma assinatura após pagamento bem-sucedido
    
    Args:
        assinatura_id: ID da assinatura
        gateway_payment_id: ID do pagamento no gateway
        db: Sessão do banco de dados
    
    Returns:
        Assinatura renovada
    """
    from datetime import datetime, timedelta
    
    assinatura = db.query(models.Assinatura).filter(
        models.Assinatura.id == assinatura_id
    ).first()
    
    if not assinatura:
        raise ValueError(f"Assinatura {assinatura_id} não encontrada")
    
    # Atualizar status e datas
    assinatura.status = models.StatusAssinaturaEnum.ATIVA
    
    # Estender expiração por 30 dias
    if assinatura.expira_em and assinatura.expira_em > datetime.utcnow():
        # Se ainda não expirou, adiciona 30 dias à data de expiração
        assinatura.expira_em = assinatura.expira_em + timedelta(days=30)
    else:
        # Se já expirou, define nova expiração a partir de agora
        assinatura.expira_em = datetime.utcnow() + timedelta(days=30)
    
    # Próximo pagamento em 30 dias
    assinatura.proximo_pagamento = assinatura.expira_em
    assinatura.tentativas_cobranca = 0
    assinatura.gateway_subscription_id = gateway_payment_id
    
    db.commit()
    db.refresh(assinatura)
    
    # Registrar no histórico
    registrar_evento_historico(
        assinatura_id=assinatura.id,
        acao="RENOVADA",
        valor_pago=float(assinatura.plano.preco_mensal),
        detalhes={
            "gateway_payment_id": gateway_payment_id,
            "nova_expiracao": assinatura.expira_em.isoformat()
        },
        criado_por="sistema",
        db=db
    )
    
    return assinatura


def verificar_limite_plano(usuario_id: int, recurso: str, db: Session) -> bool:
    """
    Verifica se o usuário está dentro dos limites do plano para determinado recurso
    
    Args:
        usuario_id: ID do usuário
        recurso: Tipo de recurso ('projetos', 'lotes', 'storage')
        db: Sessão do banco de dados
    
    Returns:
        True se pode usar o recurso, False se atingiu o limite
    
    Raises:
        ValueError: Se não houver assinatura ativa
    """
    assinatura = obter_assinatura_atual(usuario_id, db)
    
    if not assinatura:
        raise ValueError("Usuário não possui assinatura ativa")
    
    plano = assinatura.plano
    
    if recurso == "projetos":
        if plano.max_projetos == -1:
            return True  # Ilimitado
        
        count_projetos = db.query(models.Projeto).filter(
            models.Projeto.id.in_(
                db.query(models.Lote.projeto_id).filter(
                    models.Lote.id == usuario_id
                )
            )
        ).count()
        
        return count_projetos < plano.max_projetos
    
    elif recurso == "lotes":
        if plano.max_lotes_por_projeto == -1:
            return True  # Ilimitado
        
        # Esta validação seria feita no contexto de um projeto específico
        return True
    
    return True


def registrar_evento_historico(
    assinatura_id: int,
    acao: str,
    plano_anterior_id: int = None,
    plano_novo_id: int = None,
    valor_pago: float = None,
    detalhes: dict = None,
    criado_por: str = "sistema",
    db: Session = None
):
    """
    Registra um evento no histórico de assinaturas
    
    Args:
        assinatura_id: ID da assinatura
        acao: Ação realizada (CRIADA, RENOVADA, UPGRADE, DOWNGRADE, CANCELADA, SUSPENSA)
        plano_anterior_id: ID do plano anterior (para upgrades/downgrades)
        plano_novo_id: ID do novo plano
        valor_pago: Valor pago (para renovações)
        detalhes: Detalhes adicionais em JSON
        criado_por: Identificação de quem fez a ação
        db: Sessão do banco de dados
    """
    historico = models.HistoricoAssinatura(
        assinatura_id=assinatura_id,
        acao=acao,
        plano_anterior_id=plano_anterior_id,
        plano_novo_id=plano_novo_id,
        valor_pago=valor_pago,
        detalhes=detalhes,
        criado_por=criado_por
    )
    
    db.add(historico)
    db.commit()
    
    return historico


# ==================== VALIDAÇÕES GEOESPACIAIS ADICIONAIS ====================

def validate_lote_within_gleba(lote_wkt: str, projeto_id: int, db: Session) -> dict:
    """
    Valida se o lote está completamente dentro da gleba do projeto.
    
    Returns:
        dict: {"valid": bool, "message": str, "area_fora_percent": float}
    """
    # Buscar geometria da gleba
    stmt = text(f"""
        SELECT ST_AsText(geom) 
        FROM projetos 
        WHERE id = :pid AND geom IS NOT NULL
    """)
    
    gleba_result = db.execute(stmt, {"pid": projeto_id}).fetchone()
    
    if not gleba_result or not gleba_result[0]:
        return {
            "valid": True, 
            "message": "Projeto sem gleba definida - validação ST_Within ignorada",
            "area_fora_percent": 0.0
        }
    
    gleba_wkt = gleba_result[0]
    
    # Verificar se está dentro
    stmt_within = text(f"""
        SELECT ST_Within(
            ST_GeomFromText(:lote_wkt, {SRID_OFICIAL}),
            ST_GeomFromText(:gleba_wkt, {SRID_OFICIAL})
        )
    """)
    
    is_within = db.execute(stmt_within, {
        "lote_wkt": lote_wkt,
        "gleba_wkt": gleba_wkt
    }).scalar()
    
    if not is_within:
        # Calcular % da área que está fora
        stmt_diff = text(f"""
            SELECT 
                ST_Area(ST_Difference(
                    ST_GeomFromText(:lote_wkt, {SRID_OFICIAL})::geography,
                    ST_GeomFromText(:gleba_wkt, {SRID_OFICIAL})::geography
                )) / 
                ST_Area(ST_GeomFromText(:lote_wkt, {SRID_OFICIAL})::geography) * 100
        """)
        
        area_fora_percent = db.execute(stmt_diff, {
            "lote_wkt": lote_wkt,
            "gleba_wkt": gleba_wkt
        }).scalar() or 0.0
        
        return {
            "valid": False,
            "message": f"ERRO: {area_fora_percent:.1f}% do lote está fora da gleba do projeto",
            "area_fora_percent": float(area_fora_percent)
        }
    
    return {"valid": True, "message": "Lote está dentro da gleba", "area_fora_percent": 0.0}


def get_confrontantes(lote_id: int, db: Session) -> list:
    """
    Retorna lista de lotes que compartilham divisa (ST_Touches) com o lote especificado.
    
    Returns:
        list: [{"id": int, "nome_cliente": str, "shared_length_m": float}]
    """
    stmt = text(f"""
        SELECT 
            l2.id,
            l2.nome_cliente,
            ST_Length(
                ST_Intersection(l1.geom::geography, l2.geom::geography)
            ) as shared_length_m
        FROM lotes l1
        JOIN lotes l2 ON l1.projeto_id = l2.projeto_id
        WHERE l1.id = :lote_id
        AND l2.id != :lote_id
        AND ST_Touches(l1.geom, l2.geom)
        ORDER BY shared_length_m DESC
    """)
    
    result = db.execute(stmt, {"lote_id": lote_id}).fetchall()
    
    confrontantes = []
    for row in result:
        confrontantes.append({
            "id": row[0],
            "nome_cliente": row[1] or "Cliente Não Informado",
            "shared_length_m": round(float(row[2]), 2)
        })
    
    return confrontantes


def calcular_area_geodesica(wkt_geometry: str, db: Session) -> dict:
    """
    Calcula área e perímetro usando geografia geodésica (SIRGAS 2000).
    
    Returns:
        dict: {"area_ha": float, "area_m2": float, "perimetro_m": float}
    """
    stmt_metrics = text(f"""
        SELECT 
            ST_Area(ST_GeomFromText(:wkt, {SRID_OFICIAL})::geography) as area_m2,
            ST_Perimeter(ST_GeomFromText(:wkt, {SRID_OFICIAL})::geography) as perimetro_m
    """)
    
    result = db.execute(stmt_metrics, {"wkt": wkt_geometry}).fetchone()
    
    area_m2 = float(result[0])
    perimetro_m = float(result[1])
    
    return {
        "area_ha": round(area_m2 / 10000.0, 4),
        "area_m2": round(area_m2, 2),
        "perimetro_m": round(perimetro_m, 2)
    }
