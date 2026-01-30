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

    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    return db_projeto
