from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, text, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
import bcrypt
from datetime import datetime
from typing import Optional
from database import Base


# ==================== MODELO DE USUÁRIOS (AUTENTICAÇÃO) ====================

class UserRole(enum.Enum):
    """Enum para roles de usuário"""
    ADMIN = "ADMIN"
    TOPOGRAFO = "TOPOGRAFO"
    CLIENTE = "CLIENTE"
    AGRICULTOR = "AGRICULTOR"


class User(Base):
    """
    Modelo de usuário com autenticação JWT
    
    Suporta 4 perfis (roles):
    - ADMIN: Administrador do sistema
    - TOPOGRAFO: Profissional técnico (cria projetos/lotes)
    - CLIENTE: Proprietário de terra
    - AGRICULTOR: Produtor rural
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENTE)
    
    # Perfil
    avatar = Column(String(500))
    telefone = Column(String(20))
    cpf_cnpj = Column(String(20))
    
    # Controle de Acesso
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(255))
    password_reset_token = Column(String(255))
    password_reset_expires = Column(TIMESTAMP)
    
    # Timestamps
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    atualizado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    ultimo_login = Column(TIMESTAMP)
    
    def set_password(self, password: str) -> None:
        """
        Hasheia a senha usando bcrypt (rounds=12)
        
        Args:
            password: Senha em texto plano
        """
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """
        Verifica se a senha fornecida corresponde ao hash armazenado
        
        Args:
            password: Senha em texto plano
            
        Returns:
            True se a senha estiver correta, False caso contrário
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    def update_last_login(self) -> None:
        """Atualiza timestamp do último login"""
        self.ultimo_login = datetime.utcnow()
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        Converte o modelo para dicionário
        
        Args:
            include_sensitive: Se True, inclui dados sensíveis (use com cuidado)
            
        Returns:
            Dict com dados do usuário
        """
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role.value if self.role else None,
            "avatar": self.avatar,
            "telefone": self.telefone,
            "is_active": self.is_active,
            "email_verified": self.email_verified,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "ultimo_login": self.ultimo_login.isoformat() if self.ultimo_login else None
        }
        
        if include_sensitive:
            data["cpf_cnpj"] = self.cpf_cnpj
            data["password_hash"] = self.password_hash
        
        return data
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.value}')>"


# ==================== MODELO DE REFERÊNCIA SIGEF/INCRA ====================

class SigefIncra(Base):
    __tablename__ = "sigef_incra"
    # Tabela de referencia oficial (Read-only para a aplicacao)
    id = Column(Integer, primary_key=True)
    codigo_imovel = Column(String(50))
    detentor = Column(String(200))
    geom = Column(JSON, nullable=True)  # JSONB geometry (WKT format)

class Projeto(Base):
    __tablename__ = "projetos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String, nullable=True)
    tipo = Column(String(50), default='INDIVIDUAL') # Enum no banco, string aqui por simplicidade
    status = Column(String(50), default='RASCUNHO')
    
    # Relacionamento com usuário criador
    criado_por = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    atualizado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    
    # Relacao com Lotes e User
    lotes = relationship("Lote", back_populates="projeto", cascade="all, delete-orphan")
    criador = relationship("User", foreign_keys=[criado_por])

class Lote(Base):
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=True)
    
    # Relacionamento com usuário criador
    criado_por = Column(Integer, ForeignKey("users.id"), nullable=True)
    
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
    geom = Column(JSON, nullable=True)  # JSONB geometry (WKT format)
    area_ha = Column(Numeric(10, 4))
    perimetro_m = Column(Numeric(10, 2))
    
    # Workflow
    status = Column(String(50), default='PENDENTE')
    validacao_metadata = Column(JSON, nullable=True) # Logs de sobreposicao etc
    contrato_url = Column(String, nullable=True)
    
    # Relationships
    projeto = relationship("Projeto", back_populates="lotes")
    pagamentos = relationship("Pagamento", back_populates="lote")

    @property
    def proprietario(self):
        return self.nome_cliente

    @property
    def warnings(self):
        if self.validacao_metadata and isinstance(self.validacao_metadata, dict):
            return self.validacao_metadata.get("warnings", [])
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
    usuario_id = Column(Integer, ForeignKey("users.id"), index=True)  # Vincula ao cliente/topógrafo
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
    metadata_json = Column(JSON)
    tentativas_cobranca = Column(Integer, default=0)
    ultima_tentativa_cobranca = Column(TIMESTAMP)
    
    # Timestamps
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    atualizado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    
    # Relationships
    usuario = relationship("User")
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


# ==================== MODELOS DAS NOVAS FEATURES ====================

class WMSLayer(Base):
    """Camadas WMS para visualização (SIGEF, CAR, FUNAI)"""
    __tablename__ = "wms_layers"
    
    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), index=True)
    name = Column(String(100), nullable=False)
    url = Column(String, nullable=False)
    visible = Column(Boolean, default=True)
    opacity = Column(Numeric(3, 2), default=1.0)
    
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    atualizado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class ChatMessage(Base):
    """Mensagens de chat entre topógrafo e cliente"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"), index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    sender_role = Column(String(20), nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), index=True)


class StatusHistory(Base):
    """Histórico de mudanças de status (Timeline)"""
    __tablename__ = "status_history"
    
    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lotes.id"), index=True)
    status_anterior = Column(String(50))
    status_novo = Column(String(50), nullable=False)
    observacao = Column(String)
    alterado_por = Column(Integer, ForeignKey("users.id"))
    
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class Arquivo(Base):
    """Metadados de arquivos (KML, GeoJSON, PDF, Excel)"""
    __tablename__ = "arquivos"
    
    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lotes.id"), index=True)
    nome = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=False)
    tamanho_kb = Column(Integer)
    conteudo_base64 = Column(String)
    url_externa = Column(String)
    metadata = Column(JSON)
    
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))



