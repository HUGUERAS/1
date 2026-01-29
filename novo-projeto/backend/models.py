from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from database import Base

class SigefIncra(Base):
    __tablename__ = "sigef_incra"
    # Tabela de referencia oficial (Read-only para a aplicacao)
    id = Column(Integer, primary_key=True)
    codigo_imovel = Column(String(50))
    detentor = Column(String(200))
    geom = Column(Geometry("POLYGON", srid=4674))

class Projeto(Base):
    __tablename__ = "projetos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String, nullable=True)
    matricula_mae = Column(String(50))
    # Geometria da Fazenda Original (Poligono Pai)
    geom = Column(Geometry("POLYGON", srid=4674)) 
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    
    # Relacao com Lotes
    lotes = relationship("Lote", back_populates="projeto")

class Lote(Base):
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=True)
    matricula = Column(String(50))
    proprietario = Column(String(100))
    geom = Column(Geometry("POLYGON", srid=4674))
    area_ha = Column(Numeric(10, 4))
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    
    projeto = relationship("Projeto", back_populates="lotes")
