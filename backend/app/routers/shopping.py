from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from app.config import DEFAULT_MAPPEDIN_URL
from app.database import get_db
from typing import Dict
from app.busca import normalizar
from app.models import Loja, PontoInteresse, Rota, Totem
from app.routers.vitrine import buscar_produtos
from app.schemas import (
    LojaOut,
    LojaPerfilOut,
    LojaResumoOut,
    PontoInteresseOut,
    ProdutoVitrineOut,
    RotaOut,
    TotemOut,
)

router = APIRouter(prefix="/api", tags=["Shopping, Mapa 3D & Rotas (RN03-RN05, RN11)"])


def _resumir_loja(loja: Loja, produtos: List[ProdutoVitrineOut]) -> LojaResumoOut:
    promos = [p for p in produtos if p.percentual_desconto > 0]
    categorias: List[str] = []
    for p in produtos:
        if p.categoria not in categorias:
            categorias.append(p.categoria)
    return LojaResumoOut(
        **LojaOut.model_validate(loja).model_dump(),
        total_produtos=len(produtos),
        total_promocoes=len(promos),
        maior_desconto=max((p.percentual_desconto for p in promos), default=0),
        menor_preco=min((p.preco_final for p in produtos), default=None),
        categorias_produtos=categorias,
        atualizado_em=max((p.atualizado_em for p in produtos), default=None),
    )


@router.get("/lojas", response_model=List[LojaResumoOut])
def listar_lojas(
    q: Optional[str] = Query(default=None, description="Nome, categoria ou descrição da loja"),
    pavimento: Optional[str] = Query(default=None),
    categoria: Optional[str] = Query(default=None),
    com_promocao: bool = Query(default=False, description="Apenas lojas com promoções ativas"),
    totem_id: int = Query(default=1),
    db: Session = Depends(get_db),
):
    lojas = db.query(Loja).order_by(Loja.id).all()
    if pavimento:
        lojas = [l for l in lojas if normalizar(pavimento) in normalizar(l.pavimento)]
    if categoria:
        lojas = [l for l in lojas if normalizar(categoria) in normalizar(l.categoria)]
    if q:
        termo = normalizar(q).strip()
        lojas = [
            l for l in lojas
            if termo in normalizar(l.nome) or termo in normalizar(l.categoria) or termo in normalizar(l.descricao)
        ]

    produtos = buscar_produtos(db, totem_id=totem_id)
    por_loja: Dict[int, List[ProdutoVitrineOut]] = {}
    for p in produtos:
        por_loja.setdefault(p.loja_id, []).append(p)

    resumos = [_resumir_loja(l, por_loja.get(l.id, [])) for l in lojas]
    if com_promocao:
        resumos = [r for r in resumos if r.total_promocoes > 0]
    return resumos


@router.get("/lojas/{loja_id}", response_model=LojaOut)
def obter_loja(loja_id: int, db: Session = Depends(get_db)):
    loja = db.query(Loja).filter(Loja.id == loja_id).first()
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada.")
    return loja


@router.get("/lojas/{loja_id}/perfil", response_model=LojaPerfilOut)
def obter_perfil_loja(
    loja_id: int,
    totem_id: int = Query(default=1, description="Totem de origem para a rota (RN05)"),
    db: Session = Depends(get_db),
):
    """
    Perfil público da loja: dados e localização, rota a partir do totem,
    promoções em destaque e todos os produtos ativos atualizados pelo lojista.
    """
    loja = db.query(Loja).filter(Loja.id == loja_id).first()
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada.")

    produtos = buscar_produtos(db, loja_id=loja_id, ordenar_por="recente", totem_id=totem_id)
    destaques = sorted(
        (p for p in produtos if p.percentual_desconto > 0),
        key=lambda p: (-p.percentual_desconto, p.preco_final),
    )[:6]

    return LojaPerfilOut(
        loja=_resumir_loja(loja, produtos),
        rota=montar_rota(db, totem_id, loja_id),
        destaques=destaques,
        produtos=produtos,
    )


@router.get("/totens", response_model=List[TotemOut])
def listar_totens(db: Session = Depends(get_db)):
    return db.query(Totem).order_by(Totem.id).all()


@router.get("/totens/{totem_id}", response_model=TotemOut)
def obter_totem(totem_id: int, db: Session = Depends(get_db)):
    totem = db.query(Totem).filter(Totem.id == totem_id).first()
    if not totem:
        # Fallback para Totem 1 caso um ID não cadastrado seja informado na URL
        totem = db.query(Totem).filter(Totem.id == 1).first()
    if not totem:
        raise HTTPException(status_code=404, detail="Totem não encontrado.")
    return totem


@router.get("/pontos-interesse", response_model=List[PontoInteresseOut])
def listar_pontos_interesse(
    pavimento: Optional[str] = Query(default=None),
    tipo: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(PontoInteresse)
    if pavimento:
        query = query.filter(PontoInteresse.pavimento.ilike(f"%{pavimento}%"))
    if tipo:
        query = query.filter(PontoInteresse.tipo.ilike(f"%{tipo}%"))
    return query.order_by(PontoInteresse.id).all()


@router.get("/rotas", response_model=RotaOut)
def obter_rota_para_loja(
    totem_id: int = Query(default=1, description="ID do totem de origem fixa (RN05)"),
    loja_id: int = Query(..., description="ID da loja de destino"),
    db: Session = Depends(get_db),
):
    """
    RN05: Rotas iniciadas no totem consideram sempre a posição fixa cadastrada para aquele equipamento (:totemId).
    """
    rota = montar_rota(db, totem_id, loja_id)
    if rota is None:
        raise HTTPException(status_code=404, detail="Loja de destino não encontrada.")
    return rota


def montar_rota(db: Session, totem_id: int, loja_id: int) -> Optional[RotaOut]:
    """Rota cadastrada do totem até a loja, ou rota calculada de fallback."""
    totem = db.query(Totem).filter(Totem.id == totem_id).first()
    if not totem:
        totem = db.query(Totem).filter(Totem.id == 1).first()

    loja = db.query(Loja).filter(Loja.id == loja_id).first()
    if not loja:
        return None

    rota = (
        db.query(Rota)
        .options(joinedload(Rota.totem_origem), joinedload(Rota.loja_destino))
        .filter(Rota.totem_origem_id == totem.id, Rota.loja_destino_id == loja.id)
        .first()
    )

    if rota:
        return RotaOut(
            id=rota.id,
            totem_origem_id=totem.id,
            loja_destino_id=loja.id,
            url_rota=rota.url_rota,
            instrucoes=rota.instrucoes,
            tempo_estimado_min=rota.tempo_estimado_min,
            totem_identificacao=totem.identificacao,
            totem_pavimento=totem.pavimento,
            totem_referencia=totem.posicao_referencia,
            loja_nome=loja.nome,
            loja_pavimento=loja.pavimento,
            loja_localizacao=loja.localizacao,
        )

    # Rota calculada de fallback quando não houver registro explícito
    mesmo_piso = totem.pavimento == loja.pavimento
    tempo = 2 if mesmo_piso else 4
    instrucoes = (
        f"Siga pelo corredor principal do {loja.pavimento} até {loja.nome} ({loja.localizacao})."
        if mesmo_piso
        else f"Utilize o elevador ou escada rolante até o {loja.pavimento} e siga para {loja.nome} ({loja.localizacao})."
    )
    return RotaOut(
        id=0,
        totem_origem_id=totem.id,
        loja_destino_id=loja.id,
        url_rota=loja.mappedin_url or DEFAULT_MAPPEDIN_URL,
        instrucoes=instrucoes,
        tempo_estimado_min=tempo,
        totem_identificacao=totem.identificacao,
        totem_pavimento=totem.pavimento,
        totem_referencia=totem.posicao_referencia,
        loja_nome=loja.nome,
        loja_pavimento=loja.pavimento,
        loja_localizacao=loja.localizacao,
    )
