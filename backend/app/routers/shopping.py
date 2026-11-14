from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from app.config import DEFAULT_MAPPEDIN_URL
from app.database import get_db
from app.models import Loja, PontoInteresse, Rota, Totem
from app.schemas import LojaOut, PontoInteresseOut, RotaOut, TotemOut

router = APIRouter(prefix="/api", tags=["Shopping, Mapa 3D & Rotas (RN03-RN05, RN11)"])


@router.get("/lojas", response_model=List[LojaOut])
def listar_lojas(
    q: Optional[str] = Query(default=None),
    pavimento: Optional[str] = Query(default=None),
    categoria: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Loja)
    if q:
        query = query.filter(
            (Loja.nome.ilike(f"%{q}%"))
            | (Loja.categoria.ilike(f"%{q}%"))
            | (Loja.descricao.ilike(f"%{q}%"))
        )
    if pavimento:
        query = query.filter(Loja.pavimento.ilike(f"%{pavimento}%"))
    if categoria:
        query = query.filter(Loja.categoria.ilike(f"%{categoria}%"))
    return query.order_by(Loja.id).all()


@router.get("/lojas/{loja_id}", response_model=LojaOut)
def obter_loja(loja_id: int, db: Session = Depends(get_db)):
    loja = db.query(Loja).filter(Loja.id == loja_id).first()
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada.")
    return loja


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
    totem = db.query(Totem).filter(Totem.id == totem_id).first()
    if not totem:
        totem = db.query(Totem).filter(Totem.id == 1).first()

    loja = db.query(Loja).filter(Loja.id == loja_id).first()
    if not loja:
        raise HTTPException(status_code=404, detail="Loja de destino não encontrada.")

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
