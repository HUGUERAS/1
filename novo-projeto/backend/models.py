from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, text, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
import enum
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


# ==================== MODELOS PAY AS YOU GO ====================

class StatusAssinaturaEnum(enum.Enum):
    """Enum para status de assinatura"""
    TRIAL = "TRIAL"
    PENDENTE = "PENDENTE"
    ATIVA = "ATIVA"
    CANCELADA = "CANCELADA"
    SUSPENSA = "SUSPENSA"
    EXPIRADA = "EXPIRADA"


class PlanoPagamento(Base):
    """Planos de assinatura disponíveis no sistema"""
    __tablename__ = "planos_pagamento"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, nullable=False)
    descricao = Column(String)
    preco_mensal = Column(Numeric(10, 2), nullable=False, default=0)
    
    # Limites de Uso
    max_projetos = Column(Integer, default=-1)  # -1 = ilimitado
    max_lotes_por_projeto = Column(Integer, default=-1)
    storage_mb = Column(Integer, default=100)
    
    # Recursos/Features
    permite_export_kml = Column(Boolean, default=False)
    permite_export_shp = Column(Boolean, default=False)
    permite_export_dxf = Column(Boolean, default=False)
    permite_api_access = Column(Boolean, default=False)
    
    # Metadata flexível
    features = Column(JSON)
    
    # Controle
    ativo = Column(Boolean, default=True)
    ordem_exibicao = Column(Integer, default=0)
    
    # Timestamps
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    atualizado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    
    # Relationships
    assinaturas = relationship("Assinatura", back_populates="plano")


class Assinatura(Base):
    """Assinaturas dos usuários aos planos"""
    __tablename__ = "assinaturas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("lotes.id"), index=True)  # Vincula ao cliente/topógrafo
    plano_id = Column(Integer, ForeignKey("planos_pagamento.id"))
    
    # Status e Ciclo de Vida
    status = Column(Enum(StatusAssinaturaEnum), default=StatusAssinaturaEnum.TRIAL)
    
    # Datas Importantes
    inicio_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    expira_em = Column(TIMESTAMP)
    cancelada_em = Column(TIMESTAMP)
    suspensa_em = Column(TIMESTAMP)
    proximo_pagamento = Column(TIMESTAMP)
    
    # Integração com Gateway de Pagamento
    gateway_subscription_id = Column(String(100), index=True)
    gateway_customer_id = Column(String(100))
    metodo_pagamento = Column(String(20))  # PIX, CARTAO, BOLETO
    
    # Histórico e Auditoria
    metadata = Column(JSON)
    tentativas_cobranca = Column(Integer, default=0)
    ultima_tentativa_cobranca = Column(TIMESTAMP)
    
    # Timestamps
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    atualizado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    
    # Relationships
    plano = relationship("PlanoPagamento", back_populates="assinaturas")
    historico = relationship("HistoricoAssinatura", back_populates="assinatura", cascade="all, delete-orphan")


class HistoricoAssinatura(Base):
    """Log de todas as alterações em assinaturas"""
    __tablename__ = "historico_assinaturas"
    
    id = Column(Integer, primary_key=True, index=True)
    assinatura_id = Column(Integer, ForeignKey("assinaturas.id"), index=True)
    
    # Ação Realizada
    acao = Column(String(50), nullable=False)  # CRIADA, RENOVADA, UPGRADE, DOWNGRADE, CANCELADA, SUSPENSA
    
    # Mudança de Plano (se aplicável)
    plano_anterior_id = Column(Integer, ForeignKey("planos_pagamento.id"))
    plano_novo_id = Column(Integer, ForeignKey("planos_pagamento.id"))
    
    # Valores
    valor_pago = Column(Numeric(10, 2))
    
    # Detalhes Adicionais
    detalhes = Column(JSON)
    
    # Auditoria
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    criado_por = Column(String(100))  # Email/ID do usuário que fez a ação
    
    # Relationships
    assinatura = relationship("Assinatura", back_populates="historico")
