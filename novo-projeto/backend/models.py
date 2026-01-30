from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
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
    tipo = Column(String(50), default='INDIVIDUAL') # Enum no banco, string aqui por simplicidade
    status = Column(String(50), default='RASCUNHO')
    
    # REMOVIDO: Geometria e Matricula da Mae (Simplificação)
    
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    atualizado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    
    # Relacao com Lotes
    lotes = relationship("Lote", back_populates="projeto", cascade="all, delete-orphan")

class Lote(Base):
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=True)
    
    # Dados Cliente
    nome_cliente = Column(String(150))
    email_cliente = Column(String(150))
    telefone_cliente = Column(String(20))
    cpf_cnpj_cliente = Column(String(20))
    
    # Acesso
    token_acesso = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True)
    link_expira_em = Column(TIMESTAMP, nullable=True)

    # Tecnico
    matricula = Column(String(50))
    geom = Column(Geometry("POLYGON", srid=4674))
    area_ha = Column(Numeric(10, 4))
    perimetro_m = Column(Numeric(10, 2))
    
    # Workflow
    status = Column(String(50), default='PENDENTE')
    metadata_validacao = Column(JSON, nullable=True) # Logs de sobreposicao etc
    contrato_url = Column(String, nullable=True)
    
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    atualizado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    
    projeto = relationship("Projeto", back_populates="lotes")
    pagamentos = relationship("Pagamento", back_populates="lote")

    @property
    def proprietario(self):
        return self.nome_cliente

    @property
    def warnings(self):
        if self.metadata_validacao and isinstance(self.metadata_validacao, dict):
            return self.metadata_validacao.get("warnings", [])
        return []


class Pagamento(Base):
    __tablename__ = "pagamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lotes.id"))
    valor_total = Column(Numeric(10, 2), nullable=False)
    valor_pago = Column(Numeric(10, 2), default=0)
    status = Column(String(20), default='PENDENTE')
    gateway_id = Column(String(100))
    data_pagamento = Column(TIMESTAMP)
    
    lote = relationship("Lote", back_populates="pagamentos")
