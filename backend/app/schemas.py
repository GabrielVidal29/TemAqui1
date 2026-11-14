from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class LojaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: Optional[str] = None
    categoria: str
    pavimento: str
    mappedin_url: str
    localizacao: str


class PromocaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    produto_id: int
    preco_promocional: float
    data_inicio: datetime
    data_fim: datetime
    ativa: bool


class ProdutoVitrineOut(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    categoria: str
    preco_original: float
    preco_promocional: Optional[float] = None
    preco_final: float
    percentual_desconto: int = 0
    imagem_url: str
    ativo: bool
    atualizado_em: datetime
    atualizado_formatado: str
    validade_promocao: Optional[str] = None
    loja_id: int
    loja: LojaOut
    tempo_estimado_min: int = 2
    instrucoes_rota: Optional[str] = None


class RotaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    totem_origem_id: int
    loja_destino_id: int
    url_rota: str
    instrucoes: str
    tempo_estimado_min: int
    totem_identificacao: Optional[str] = None
    totem_pavimento: Optional[str] = None
    totem_referencia: Optional[str] = None
    loja_nome: Optional[str] = None
    loja_pavimento: Optional[str] = None
    loja_localizacao: Optional[str] = None


class TotemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    identificacao: str
    pavimento: str
    posicao_referencia: str


class PontoInteresseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    tipo: str
    pavimento: str
    localizacao: str


class ProdutoDetalheOut(BaseModel):
    produto: ProdutoVitrineOut
    rota: Optional[RotaOut] = None
    similares: List[ProdutoVitrineOut] = []


class LoginLojistaRequest(BaseModel):
    email: str
    senha: str


class LojistaProfileOut(BaseModel):
    id: int
    nome: str
    email: str
    loja_id: int
    loja: LojaOut


class LoginLojistaResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    lojista: LojistaProfileOut


class ProdutoCreateRequest(BaseModel):
    nome: str = Field(..., min_length=2, max_length=160)
    descricao: Optional[str] = ""
    categoria: str = Field(..., min_length=2, max_length=80)
    preco: float = Field(..., gt=0)
    preco_promocional: Optional[float] = Field(default=None, gt=0)
    imagem_url: Optional[str] = "/assets/tenis-sprint.svg"
    ativo: bool = True


class ProdutoUpdateRequest(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    preco: Optional[float] = Field(default=None, gt=0)
    preco_promocional: Optional[float] = None
    remover_promocao: bool = False
    imagem_url: Optional[str] = None
    ativo: Optional[bool] = None


class ProdutoStatusPatchRequest(BaseModel):
    ativo: bool


class DashboardLojistaOut(BaseModel):
    loja: LojaOut
    lojista: LojistaProfileOut
    kpis: dict
    produtos: List[ProdutoVitrineOut]
