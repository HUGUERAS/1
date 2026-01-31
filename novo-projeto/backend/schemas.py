from pydantic import BaseModel, validator
from typing import List, Tuple, Optional, Any, Dict
from datetime import datetime
from uuid import UUID
from enum import Enum

class LoteBase(BaseModel):
    matricula: str
    proprietario: str
    projeto_id: Optional[int] = None

class LoteCreate(LoteBase):
    coordinates: List[Tuple[float, float]] 

    @validator("coordinates")
    def validate_polygon_closure(cls, v):
        if len(v) < 3:
            raise ValueError("Um poligono precisa de pelo menos 3 pontos")
        if v[0] != v[-1]:
            v.append(v[0])
        return v

class LoteResponse(LoteBase):
    id: int
    area_ha: Optional[float] = None
    perimetro_m: Optional[float] = None
    warnings: List[str] = []
    metadata_validacao: Optional[Dict[str, Any]] = None
    token_acesso: Optional[UUID] = None
    criado_em: Optional[datetime]
    
    class Config:
        from_attributes = True

class ProjetoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    tipo: Optional[str] = "INDIVIDUAL"

class ProjetoCreate(ProjetoBase):
    coordinates: List[Tuple[float, float]] = [] 

    @validator("coordinates")
    def validate_polygon_closure(cls, v):
        if not v:
            return v
        if len(v) < 3:
            raise ValueError("Um poligono precisa de pelo menos 3 pontos")
        if v[0] != v[-1]:
            v.append(v[0])
        return v

class ProjetoResponse(ProjetoBase):
    id: int
    criado_em: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== SCHEMAS PAY AS YOU GO ====================

class StatusAssinatura(str, Enum):
    """Enum para status de assinatura"""
    TRIAL = "TRIAL"
    PENDENTE = "PENDENTE"
    ATIVA = "ATIVA"
    CANCELADA = "CANCELADA"
    SUSPENSA = "SUSPENSA"
    EXPIRADA = "EXPIRADA"


class PlanoBase(BaseModel):
    """Schema base para Plano de Pagamento"""
    nome: str
    descricao: Optional[str] = None
    preco_mensal: float
    max_projetos: int = -1
    max_lotes_por_projeto: int = -1
    storage_mb: int = 100
    permite_export_kml: bool = False
    permite_export_shp: bool = False
    permite_export_dxf: bool = False
    permite_api_access: bool = False


class PlanoResponse(PlanoBase):
    """Schema de resposta para Plano de Pagamento"""
    id: int
    features: Optional[Dict[str, Any]] = None
    ativo: bool = True
    ordem_exibicao: int = 0
    criado_em: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AssinaturaCreate(BaseModel):
    """Schema para criar assinatura"""
    plano_id: int
    usuario_id: int
    metodo_pagamento: Optional[str] = None  # PIX, CARTAO, BOLETO


class AssinaturaResponse(BaseModel):
    """Schema de resposta para Assinatura"""
    id: int
    usuario_id: int
    plano_id: int
    status: StatusAssinatura
    inicio_em: datetime
    expira_em: Optional[datetime] = None
    proximo_pagamento: Optional[datetime] = None
    gateway_subscription_id: Optional[str] = None
    metodo_pagamento: Optional[str] = None
    
    class Config:
        from_attributes = True


class AssinaturaComPlano(AssinaturaResponse):
    """Schema de resposta para Assinatura com detalhes do plano"""
    plano: PlanoResponse
    
    class Config:
        from_attributes = True


class AssinaturaAtualResponse(BaseModel):
    """Schema para resposta da assinatura atual com métricas de uso"""
    assinatura: AssinaturaComPlano
    limites: Dict[str, Any]  # projetos_usados, projetos_limite, storage_usado_mb, etc
    dias_restantes: Optional[int] = None
    
    class Config:
        from_attributes = True


class AlterarPlanoRequest(BaseModel):
    """Schema para alterar plano de uma assinatura"""
    novo_plano_id: int


class HistoricoAssinaturaResponse(BaseModel):
    """Schema de resposta para Histórico de Assinatura"""
    id: int
    assinatura_id: int
    acao: str
    plano_anterior_id: Optional[int] = None
    plano_novo_id: Optional[int] = None
    valor_pago: Optional[float] = None
    detalhes: Optional[Dict[str, Any]] = None
    criado_em: datetime
    criado_por: Optional[str] = None
    
    class Config:
        from_attributes = True
