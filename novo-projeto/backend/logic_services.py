from sqlalchemy.orm import Session
from sqlalchemy import text
from shapely.geometry import Polygon
from shapely import wkt
import models

def validate_geometry_rules(new_polygon_wkt: str, projeto_id: int, db: Session):
    """
    Agente 2: Validador Real de Geometria
    Executa queries espaciais reais no PostGIS. Sem mocks.
    """
    
    # Validacao SIGEF/INCRA
    stmt_sigef = text("""
        SELECT codigo_imovel, detentor
        FROM sigef_incra 
        WHERE ST_Intersects(geom, ST_GeomFromText(:wkt, 4674))
        AND ST_Area(ST_Intersection(geom, ST_GeomFromText(:wkt, 4674))) > 0.0000001
    """)
    
    conflitos_sigef = db.execute(stmt_sigef, {"wkt": new_polygon_wkt}).fetchall()
    
    if conflitos_sigef:
        detalhes = ", ".join([f"{row[0]} ({row[1]})" for row in conflitos_sigef])
        return True, f"CRITICO: Sobreposicao detectada com area federal/certificada: {detalhes}"

    # Validacao Interna
    if projeto_id:
        stmt_vizinhos = text("""
            SELECT proprietario
            FROM lotes
            WHERE projeto_id = :pid
            AND ST_Intersects(geom, ST_GeomFromText(:wkt, 4674))
            AND ST_Area(ST_Intersection(geom, ST_GeomFromText(:wkt, 4674))) > 0.0000001
        """)
        
        conflitos_vizinhos = db.execute(stmt_vizinhos, {"wkt": new_polygon_wkt, "pid": projeto_id}).fetchall()
        
        if conflitos_vizinhos:
            nomes = ", ".join([r[0] for r in conflitos_vizinhos])
            return True, f"Sobreposicao com lote vizinho detectada: {nomes}. Use a ferramenta Snap para corrigir."

    return False, ""

def create_lote_logic(lote_data, db: Session):
    coords_fixed = [(p[1], p[0]) for p in lote_data.coordinates]
    poly = Polygon(coords_fixed)
    if not poly.is_valid:
        poly = poly.buffer(0)
    wkt_str = poly.wkt
    
    has_error, msg = validate_geometry_rules(wkt_str, lote_data.projeto_id, db)
    if has_error:
        raise ValueError(msg)
    
    db_lote = models.Lote(
        matricula=lote_data.matricula,
        proprietario=lote_data.proprietario,
        projeto_id=lote_data.projeto_id,
        geom=wkt_str
    )
    
    db.add(db_lote)
    db.commit()
    db.refresh(db_lote)
    return db_lote

def create_projeto_logic(projeto_data, db: Session):
    # Handle optional coordinates for Project container
    if not projeto_data.coordinates:
         # Create project without geometry? Or generic placeholder?
         # Check model: geom is geometry(POLYGON,4674). Can be nullable in DB?
         # In models.py: geom = Column(Geometry("POLYGON", srid=4674)) default nullable=True in SQLAlchemy unless nullable=False speficied.
         # So we can create without geom if needed.
         wkt_str = None
    else:
        coords_fixed = [(p[1], p[0]) for p in projeto_data.coordinates]
        poly = Polygon(coords_fixed)
        if not poly.is_valid:
            poly = poly.buffer(0)
        wkt_str = poly.wkt

        # Validar se o Projeto invade terras indigenas/SIGEF (Regra de Ouro)
        stmt_sigef = text("""
            SELECT codigo_imovel, detentor
            FROM sigef_incra 
            WHERE ST_Intersects(geom, ST_GeomFromText(:wkt, 4674))
            AND ST_Area(ST_Intersection(geom, ST_GeomFromText(:wkt, 4674))) > 0.0000001
        """)
        conflitos = db.execute(stmt_sigef, {"wkt": wkt_str}).fetchall()
        if conflitos:
            raise ValueError(f"O Projeto sobrepoe area certificada: {conflitos[0][0]}")

    db_projeto = models.Projeto(
        nome=projeto_data.nome,
        descricao=projeto_data.descricao,
        matricula_mae=projeto_data.matricula_mae,
        geom=wkt_str
    )

    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    return db_projeto
