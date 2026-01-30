from pydantic import BaseModel, validator
from typing import List, Tuple, Optional, Any, Dict
from datetime import datetime
from uuid import UUID

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
