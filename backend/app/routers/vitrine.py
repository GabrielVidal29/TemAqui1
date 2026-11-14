from datetime import datetime
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session, joinedload
from app.busca import interpretar, normalizar, pontuar
from app.database import get_db
from app.models import ImagemProduto, Loja, Produto, Promocao, Rota
from app.schemas import CategoriaResumoOut, LojaOut, ProdutoDetalheOut, ProdutoVitrineOut, RotaOut

router = APIRouter(prefix="/api/produtos", tags=["Vitrine & Comparação (Público - RN02)"])


def serialize_produto(
    prod: Produto, db: Session, totem_id: int = 1, rotas: Optional[Dict[int, Rota]] = None
) -> ProdutoVitrineOut:
    now = datetime.now()
    promo_ativa: Optional[Promocao] = None
    for p in prod.promocoes:
        if p.ativa and p.data_fim >= now - (now - prod.atualizado_em):
            promo_ativa = p
            break

    preco_original = round(float(prod.preco), 2)
    if promo_ativa and promo_ativa.preco_promocional < preco_original:
        preco_promo = round(float(promo_ativa.preco_promocional), 2)
        preco_final = preco_promo
        desconto = round(((preco_original - preco_promo) / preco_original) * 100)
        validade = promo_ativa.data_fim.strftime("%d/%m")
    else:
        preco_promo = None
        preco_final = preco_original
        desconto = 0
        validade = None

    if rotas is not None:
        rota = rotas.get(prod.loja_id)
    else:
        rota = (
            db.query(Rota)
            .filter(Rota.totem_origem_id == totem_id, Rota.loja_destino_id == prod.loja_id)
            .first()
        )
    tempo_min = rota.tempo_estimado_min if rota else (2 if "1º" in prod.loja.pavimento else 4)
    instrucoes = (
        rota.instrucoes
        if rota
        else f"Siga até {prod.loja.nome} no {prod.loja.pavimento} ({prod.loja.localizacao})."
    )

    dt_str = prod.atualizado_em.strftime("%H:%M")
    atualizado_fmt = f"Atualizado hoje, {dt_str}"

    return ProdutoVitrineOut(
        id=prod.id,
        nome=prod.nome,
        descricao=prod.descricao,
        categoria=prod.categoria,
        preco_original=preco_original,
        preco_promocional=preco_promo,
        preco_final=preco_final,
        percentual_desconto=desconto,
        imagem_url=prod.imagem_url,
        ativo=prod.ativo,
        atualizado_em=prod.atualizado_em,
        atualizado_formatado=atualizado_fmt,
        validade_promocao=validade,
        loja_id=prod.loja_id,
        loja=LojaOut.model_validate(prod.loja),
        tempo_estimado_min=tempo_min,
        instrucoes_rota=instrucoes,
    )


def carregar_rotas(db: Session, totem_id: int) -> Dict[int, Rota]:
    """Rotas do totem indexadas por loja (evita uma consulta por produto)."""
    return {r.loja_destino_id: r for r in db.query(Rota).filter(Rota.totem_origem_id == totem_id).all()}


def _campos_busca(item: ProdutoVitrineOut) -> dict:
    return {
        "nome": normalizar(item.nome),
        "categoria": normalizar(item.categoria),
        "loja": normalizar(item.loja.nome),
        "loja_categoria": normalizar(item.loja.categoria),
        "descricao": normalizar(item.descricao),
    }


def buscar_produtos(
    db: Session,
    *,
    q: Optional[str] = None,
    categoria: Optional[str] = None,
    loja_id: Optional[int] = None,
    pavimento: Optional[str] = None,
    preco_min: Optional[float] = None,
    preco_max: Optional[float] = None,
    promocao: str = "todas",
    ordenar_por: Optional[str] = None,
    totem_id: int = 1,
) -> List[ProdutoVitrineOut]:
    """
    Busca real sobre os produtos ativos cadastrados pelos lojistas.
    RN09: produtos pausados (ativo=False) nunca aparecem.
    """
    query = (
        db.query(Produto)
        .join(Loja, Produto.loja_id == Loja.id)
        .options(joinedload(Produto.loja), joinedload(Produto.promocoes))
        .filter(Produto.ativo == True)  # noqa: E712 - RN09
    )
    if loja_id:
        query = query.filter(Produto.loja_id == loja_id)
    if pavimento and normalizar(pavimento) not in ("todos", "todas", "1o e 2o piso"):
        query = query.filter(Loja.pavimento.ilike(f"%{pavimento}%"))

    rotas = carregar_rotas(db, totem_id)
    items = [serialize_produto(p, db, totem_id=totem_id, rotas=rotas) for p in query.all()]

    # Categorias (aceita várias separadas por vírgula; compara sem acento)
    if categoria and normalizar(categoria) not in ("todas", "todos"):
        alvo = {normalizar(c.strip()) for c in categoria.split(",") if c.strip()}
        items = [i for i in items if normalizar(i.categoria) in alvo]

    # Texto livre interpretado
    consulta = interpretar(q)
    if consulta.preco_max is not None and preco_max is None:
        preco_max = consulta.preco_max
    if consulta.categorias_ocasiao:
        alvo = {normalizar(c) for c in consulta.categorias_ocasiao}
        items = [i for i in items if normalizar(i.categoria) in alvo]

    relevancia: Dict[int, int] = {}
    if consulta.termos:
        pontuados = []
        for item in items:
            campos = _campos_busca(item)
            notas = [pontuar(t, campos) for t in consulta.termos]
            pontuados.append((item, notas))
        # Todos os termos precisam bater; se nada bater, cai para "qualquer termo"
        todos = [(i, n) for i, n in pontuados if all(n)]
        escolhidos = todos or [(i, n) for i, n in pontuados if any(n)]
        items = [i for i, _ in escolhidos]
        relevancia = {i.id: sum(n) for i, n in escolhidos}

    if preco_min is not None:
        items = [i for i in items if i.preco_final >= preco_min]
    if preco_max is not None:
        items = [i for i in items if i.preco_final <= preco_max]

    if promocao == "com":
        items = [i for i in items if i.percentual_desconto > 0]
    elif promocao == "sem":
        items = [i for i in items if i.percentual_desconto == 0]

    ordem = ordenar_por or ("relevancia" if consulta.termos else "menor_preco")
    if ordem == "relevancia":
        items.sort(key=lambda x: (-relevancia.get(x.id, 0), -x.percentual_desconto, x.preco_final))
    elif ordem == "maior_preco":
        items.sort(key=lambda x: x.preco_final, reverse=True)
    elif ordem == "maior_desconto":
        items.sort(key=lambda x: (-x.percentual_desconto, x.preco_final))
    elif ordem == "recente":
        items.sort(key=lambda x: x.atualizado_em, reverse=True)
    elif ordem == "nome":
        items.sort(key=lambda x: normalizar(x.nome))
    else:  # menor_preco
        items.sort(key=lambda x: x.preco_final)

    return items


@router.get("", response_model=List[ProdutoVitrineOut])
def listar_produtos_vitrine(
    q: Optional[str] = Query(default=None, description="Busca livre: produto, loja, ocasião ou orçamento (ex.: 'tênis até R$ 350')"),
    categoria: Optional[str] = Query(default=None, description="Categoria(s) separadas por vírgula"),
    loja_id: Optional[int] = Query(default=None, description="Filtro por ID da loja"),
    pavimento: Optional[str] = Query(default=None, description="Filtro por pavimento (1º Piso, 2º Piso)"),
    preco_min: Optional[float] = Query(default=None, description="Preço mínimo"),
    preco_max: Optional[float] = Query(default=None, description="Orçamento máximo (ex: 350)"),
    promocao: str = Query(default="todas", description="todas | com (em promoção) | sem (preço normal)"),
    apenas_promocao: bool = Query(default=False, description="Compatibilidade: equivale a promocao=com"),
    ordenar_por: Optional[str] = Query(
        default=None, description="relevancia | menor_preco | maior_preco | maior_desconto | recente | nome"
    ),
    totem_id: int = Query(default=1, description="Totem de referência para cálculo de caminhada"),
    db: Session = Depends(get_db),
):
    """
    RN02: Acesso público sem login.
    RN03/RN04: Produtos vinculados a lojas com localização no mapa.
    RN09: Produtos pausados (ativo=False) NÃO aparecem na vitrine pública.
    """
    return buscar_produtos(
        db,
        q=q,
        categoria=categoria,
        loja_id=loja_id,
        pavimento=pavimento,
        preco_min=preco_min,
        preco_max=preco_max,
        promocao="com" if apenas_promocao else promocao,
        ordenar_por=ordenar_por,
        totem_id=totem_id,
    )


@router.get("/categorias", response_model=List[CategoriaResumoOut])
def listar_categorias(db: Session = Depends(get_db)):
    """Categorias com produtos ativos na vitrine, com contagem total e em promoção."""
    contagem: Dict[str, Dict[str, int]] = {}
    for item in buscar_produtos(db):
        c = contagem.setdefault(item.categoria, {"total": 0, "em_promocao": 0})
        c["total"] += 1
        if item.percentual_desconto > 0:
            c["em_promocao"] += 1
    return [
        CategoriaResumoOut(categoria=nome, total=v["total"], em_promocao=v["em_promocao"])
        for nome, v in sorted(contagem.items(), key=lambda kv: -kv[1]["total"])
    ]


@router.get("/comparar", response_model=List[ProdutoVitrineOut])
def comparar_ofertas(
    ids: Optional[str] = Query(default=None, description="IDs separados por vírgula, ex: 1,2,3"),
    categoria: Optional[str] = Query(default="Calçados", description="Categoria para comparação"),
    preco_max: Optional[float] = Query(default=None, description="Preço máximo"),
    totem_id: int = Query(default=1),
    db: Session = Depends(get_db),
):
    """
    Retorna produtos lado a lado para tela 'Compare e escolha seu caminho' (Totem) e 'Compare suas escolhas' (Mobile).
    """
    query = (
        db.query(Produto)
        .options(joinedload(Produto.loja), joinedload(Produto.promocoes))
        .filter(Produto.ativo == True)  # noqa: E712 - RN09
    )

    if ids:
        id_list = [int(x.strip()) for x in ids.split(",") if x.strip().isdigit()]
        if id_list:
            query = query.filter(Produto.id.in_(id_list))
    elif categoria:
        query = query.filter(Produto.categoria.ilike(f"%{categoria}%"))

    produtos = [serialize_produto(p, db, totem_id=totem_id) for p in query.all()]
    if preco_max is not None:
        produtos = [p for p in produtos if p.preco_final <= preco_max]

    produtos.sort(key=lambda x: x.preco_final)
    return produtos


@router.get("/{produto_id}/imagem", response_class=Response)
def obter_foto_produto(produto_id: int, db: Session = Depends(get_db)):
    """Foto enviada pelo lojista (salva no banco)."""
    imagem = db.query(ImagemProduto).filter(ImagemProduto.produto_id == produto_id).first()
    if not imagem:
        raise HTTPException(status_code=404, detail="Foto não encontrada.")
    # A URL muda a cada troca de foto (?v=...), então pode ficar em cache por bastante tempo
    return Response(
        content=imagem.conteudo,
        media_type=imagem.mime,
        headers={"Cache-Control": "public, max-age=86400", "X-Content-Type-Options": "nosniff"},
    )


@router.get("/{produto_id}", response_model=ProdutoDetalheOut)
def obter_detalhe_produto(
    produto_id: int,
    totem_id: int = Query(default=1, description="ID do totem para traçar rota fixa (RN05)"),
    db: Session = Depends(get_db),
):
    prod = (
        db.query(Produto)
        .options(joinedload(Produto.loja), joinedload(Produto.promocoes))
        .filter(Produto.id == produto_id, Produto.ativo == True)  # noqa: E712
        .first()
    )
    if not prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado ou indisponível na vitrine.")

    produto_out = serialize_produto(prod, db, totem_id=totem_id)

    rota_db = (
        db.query(Rota)
        .options(joinedload(Rota.totem_origem), joinedload(Rota.loja_destino))
        .filter(Rota.totem_origem_id == totem_id, Rota.loja_destino_id == prod.loja_id)
        .first()
    )
    rota_out = None
    if rota_db:
        rota_out = RotaOut(
            id=rota_db.id,
            totem_origem_id=rota_db.totem_origem_id,
            loja_destino_id=rota_db.loja_destino_id,
            url_rota=rota_db.url_rota,
            instrucoes=rota_db.instrucoes,
            tempo_estimado_min=rota_db.tempo_estimado_min,
            totem_identificacao=rota_db.totem_origem.identificacao,
            totem_pavimento=rota_db.totem_origem.pavimento,
            totem_referencia=rota_db.totem_origem.posicao_referencia,
            loja_nome=rota_db.loja_destino.nome,
            loja_pavimento=rota_db.loja_destino.pavimento,
            loja_localizacao=rota_db.loja_destino.localizacao,
        )

    similares_db = (
        db.query(Produto)
        .options(joinedload(Produto.loja), joinedload(Produto.promocoes))
        .filter(
            Produto.categoria == prod.categoria,
            Produto.id != prod.id,
            Produto.ativo == True,  # noqa: E712
        )
        .all()
    )
    similares_out = [serialize_produto(s, db, totem_id=totem_id) for s in similares_db]
    similares_out.sort(key=lambda x: x.preco_final)

    return ProdutoDetalheOut(produto=produto_out, rota=rota_out, similares=similares_out)
