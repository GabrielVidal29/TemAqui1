from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.auth import hash_password
from app.config import DEFAULT_MAPPEDIN_URL
from app.models import Loja, Lojista, PontoInteresse, Produto, Promocao, Rota, Totem


def run_seed(db: Session) -> None:
    if db.query(Loja).first() is not None:
        return

    now = datetime.now().replace(hour=10, minute=42, second=0, microsecond=0)
    fim_promo = now + timedelta(days=7)

    # 1. Totens Interativos do Capim Dourado Shopping
    totem_1 = Totem(
        id=1,
        identificacao="Totem Piso 1",
        pavimento="1º Piso",
        posicao_referencia="Entrada Principal",
    )
    totem_2 = Totem(
        id=2,
        identificacao="Totem Piso 2",
        pavimento="2º Piso",
        posicao_referencia="Praça de Alimentação",
    )
    db.add_all([totem_1, totem_2])
    db.flush()

    # 2. Lojas Cadastradas (Capim Dourado Shopping - Palmas, TO)
    lojas_data = [
        Loja(
            id=1,
            nome="Centauro",
            descricao="Artigos esportivos, tênis de corrida, vestuário e acessórios de treino.",
            categoria="Calçados",
            pavimento="1º Piso",
            mappedin_url=f"{DEFAULT_MAPPEDIN_URL}&store=centauro",
            localizacao="1º Pavimento • Loja 104",
        ),
        Loja(
            id=2,
            nome="Riachuelo",
            descricao="Moda feminina, masculina, calçados confortáveis e presentes.",
            categoria="Calçados",
            pavimento="1º Piso",
            mappedin_url=f"{DEFAULT_MAPPEDIN_URL}&store=riachuelo",
            localizacao="1º Pavimento • Loja 112",
        ),
        Loja(
            id=3,
            nome="Loja Esporte",
            descricao="Especialista em performance esportiva, corrida e linha outdoor.",
            categoria="Calçados",
            pavimento="2º Piso",
            mappedin_url=f"{DEFAULT_MAPPEDIN_URL}&store=loja-esporte",
            localizacao="2º Pavimento • Loja 205",
        ),
        Loja(
            id=4,
            nome="Perfumaria",
            descricao="Fragrâncias nacionais e importadas, kits de presente e cosméticos.",
            categoria="Perfumaria",
            pavimento="1º Piso",
            mappedin_url=f"{DEFAULT_MAPPEDIN_URL}&store=perfumaria",
            localizacao="1º Pavimento • Loja 108",
        ),
        Loja(
            id=5,
            nome="Acessórios",
            descricao="Bolsas em couro, carteiras, cintos e acessórios para todas as ocasiões.",
            categoria="Acessórios",
            pavimento="2º Piso",
            mappedin_url=f"{DEFAULT_MAPPEDIN_URL}&store=acessorios",
            localizacao="2º Pavimento • Loja 210",
        ),
        Loja(
            id=6,
            nome="Outback",
            descricao="Restaurante casual dining com cortes especiais e aperitivos clássicos.",
            categoria="Restaurantes",
            pavimento="2º Piso",
            mappedin_url=f"{DEFAULT_MAPPEDIN_URL}&store=outback",
            localizacao="2º Pavimento • Loja 220",
        ),
        Loja(
            id=7,
            nome="Cinemark",
            descricao="Complexo de salas de cinema 3D e XD do Capim Dourado Shopping.",
            categoria="Lazer",
            pavimento="2º Piso",
            mappedin_url=f"{DEFAULT_MAPPEDIN_URL}&store=cinemark",
            localizacao="2º Pavimento • Complexo Cinema",
        ),
    ]
    db.add_all(lojas_data)
    db.flush()

    # 3. Produtos e Promoções (Fiéis aos Prints do Figma)
    produtos_spec = [
        {
            "id": 1,
            "nome": "Tênis Sprint Run",
            "descricao": "Leveza, conforto e amortecimento para acompanhar sua rotina. Consulte tamanhos e cores disponíveis na loja.",
            "categoria": "Calçados",
            "preco": 399.90,
            "preco_promo": 299.90,
            "imagem_url": "/assets/products/tenis-sprint.svg",
            "ativo": True,
            "loja_id": 1,  # Centauro • 1º Piso
        },
        {
            "id": 2,
            "nome": "Tênis Move Comfort",
            "descricao": "Leveza, conforto e amortecimento para acompanhar sua rotina. Consulte tamanhos e cores disponíveis na loja.",
            "categoria": "Calçados",
            "preco": 349.90,
            "preco_promo": 279.90,
            "imagem_url": "/assets/products/tenis-move.svg",
            "ativo": True,
            "loja_id": 2,  # Riachuelo • 1º Piso
        },
        {
            "id": 3,
            "nome": "Tênis Urban Active",
            "descricao": "Leveza, conforto e amortecimento para acompanhar sua rotina. Consulte tamanhos e cores disponíveis na loja.",
            "categoria": "Calçados",
            "preco": 399.90,
            "preco_promo": 329.90,
            "imagem_url": "/assets/products/tenis-urban.svg",
            "ativo": True,
            "loja_id": 3,  # Loja Esporte • 2º Piso
        },
        {
            "id": 4,
            "nome": "Perfume Essencial 100 ml",
            "descricao": "Um presente especial para o dia a dia. Notas florais amadeiradas de longa duração. Consulte disponibilidade e condições na loja.",
            "categoria": "Perfumaria",
            "preco": 239.90,
            "preco_promo": 179.90,
            "imagem_url": "/assets/products/perfume-essencial.svg",
            "ativo": True,
            "loja_id": 4,  # Perfumaria • 1º Piso
        },
        {
            "id": 5,
            "nome": "Bolsa Couro Caramelo",
            "descricao": "Acabamento premium em couro legítimo com alça ajustável. Ideal para presente ou uso diário.",
            "categoria": "Acessórios",
            "preco": 339.90,
            "preco_promo": 239.90,
            "imagem_url": "/assets/products/bolsa-caramelo.svg",
            "ativo": True,
            "loja_id": 5,  # Acessórios • 2º Piso
        },
        {
            "id": 6,
            "nome": "Tênis Novo Flex",
            "descricao": "Calçados • Corrida, passeio, esporte. Solado flexível de alta tração.",
            "categoria": "Calçados",
            "preco": 399.90,
            "preco_promo": 329.90,
            "imagem_url": "/assets/products/tenis-sprint.svg",
            "ativo": True,
            "loja_id": 1,  # Centauro • 1º Piso (Print 04 Lojista)
        },
        {
            "id": 7,
            "nome": "Tênis Urban Sport",
            "descricao": "Calçados • Corrida, passeio, esporte. Modelo casual urbano.",
            "categoria": "Calçados",
            "preco": 349.90,
            "preco_promo": None,
            "imagem_url": "/assets/products/tenis-urban.svg",
            "ativo": False,  # Pausado conforme Print 04 do Painel do Lojista!
            "loja_id": 1,  # Centauro • 1º Piso
        },
    ]

    for spec in produtos_spec:
        prod = Produto(
            id=spec["id"],
            nome=spec["nome"],
            descricao=spec["descricao"],
            categoria=spec["categoria"],
            preco=spec["preco"],
            imagem_url=spec["imagem_url"],
            ativo=spec["ativo"],
            atualizado_em=now,
            loja_id=spec["loja_id"],
        )
        db.add(prod)
        db.flush()

        if spec["preco_promo"] is not None:
            promo = Promocao(
                produto_id=prod.id,
                preco_promocional=spec["preco_promo"],
                data_inicio=now - timedelta(days=1),
                data_fim=fim_promo,
                ativa=True,
            )
            db.add(promo)

    # 4. Lojistas (RN08: Cada lojista vinculado exclusivamente à sua loja)
    lojistas_data = [
        Lojista(
            id=1,
            nome="Centauro • Administrador",
            email="admin@centauro.com.br",
            senha_hash=hash_password("123456"),
            loja_id=1,
        ),
        Lojista(
            id=2,
            nome="Riachuelo • Administrador",
            email="admin@riachuelo.com.br",
            senha_hash=hash_password("123456"),
            loja_id=2,
        ),
        Lojista(
            id=3,
            nome="Loja Esporte • Administrador",
            email="admin@lojaesporte.com.br",
            senha_hash=hash_password("123456"),
            loja_id=3,
        ),
        Lojista(
            id=4,
            nome="Perfumaria • Administrador",
            email="admin@perfumaria.com.br",
            senha_hash=hash_password("123456"),
            loja_id=4,
        ),
    ]
    db.add_all(lojistas_data)

    # 5. Pontos de Interesse (Banheiros, Elevadores, Escadas, Saídas, Alimentação)
    pois_data = [
        PontoInteresse(
            nome="Elevador Central",
            tipo="elevador",
            pavimento="1º Piso",
            localizacao="Corredor Central (próximo ao Café e Moda)",
        ),
        PontoInteresse(
            nome="Elevador Central",
            tipo="elevador",
            pavimento="2º Piso",
            localizacao="Saída do Elevador — Acesso Loja Esporte e Praça de Alimentação",
        ),
        PontoInteresse(
            nome="Escadas Rolantes Principais",
            tipo="escada",
            pavimento="1º Piso",
            localizacao="Átrio Principal — Ligação 1º e 2º Piso",
        ),
        PontoInteresse(
            nome="Sanitários / WC 1º Piso",
            tipo="banheiro",
            pavimento="1º Piso",
            localizacao="Corredor Leste (ao lado da Perfumaria)",
        ),
        PontoInteresse(
            nome="Sanitários / WC 2º Piso",
            tipo="banheiro",
            pavimento="2º Piso",
            localizacao="Corredor da Praça de Alimentação",
        ),
        PontoInteresse(
            nome="Praça de Alimentação Capim Dourado",
            tipo="alimentacao",
            pavimento="2º Piso",
            localizacao="Ala Central 2º Piso",
        ),
        PontoInteresse(
            nome="Saída Principal — Entrada Norte",
            tipo="saida",
            pavimento="1º Piso",
            localizacao="Próximo ao Totem Piso 1",
        ),
    ]
    db.add_all(pois_data)

    # 6. Rotas a partir da Posição Fixa dos Totens (RN05 e RN11)
    rotas_data = [
        # Rotas a partir do Totem 1 (1º Piso - Entrada Principal)
        Rota(
            totem_origem_id=1,
            loja_destino_id=1,  # Centauro
            url_rota=f"{DEFAULT_MAPPEDIN_URL}&from=totem-1&to=centauro",
            instrucoes="Siga pelo corredor principal e vire à direita até a Loja 104 (Centauro).",
            tempo_estimado_min=2,
        ),
        Rota(
            totem_origem_id=1,
            loja_destino_id=2,  # Riachuelo
            url_rota=f"{DEFAULT_MAPPEDIN_URL}&from=totem-1&to=riachuelo",
            instrucoes="Siga pelo corredor principal à esquerda e avance até a Riachuelo (1º Piso).",
            tempo_estimado_min=2,
        ),
        Rota(
            totem_origem_id=1,
            loja_destino_id=3,  # Loja Esporte (2º Piso)
            url_rota=f"{DEFAULT_MAPPEDIN_URL}&from=totem-1&to=loja-esporte",
            instrucoes="Siga ao elevador ou escada rolante, suba ao 2º piso e vire à esquerda até a Loja Esporte.",
            tempo_estimado_min=4,
        ),
        Rota(
            totem_origem_id=1,
            loja_destino_id=4,  # Perfumaria
            url_rota=f"{DEFAULT_MAPPEDIN_URL}&from=totem-1&to=perfumaria",
            instrucoes="Siga em frente pelo corredor central por 80 metros até a Perfumaria (Loja 108).",
            tempo_estimado_min=2,
        ),
        Rota(
            totem_origem_id=1,
            loja_destino_id=5,  # Acessórios (2º Piso)
            url_rota=f"{DEFAULT_MAPPEDIN_URL}&from=totem-1&to=acessorios",
            instrucoes="Suba ao 2º piso pelo elevador central e siga pelo corredor sul até Acessórios (Loja 210).",
            tempo_estimado_min=4,
        ),
        Rota(
            totem_origem_id=1,
            loja_destino_id=6,  # Outback (2º Piso)
            url_rota=f"{DEFAULT_MAPPEDIN_URL}&from=totem-1&to=outback",
            instrucoes="Suba ao 2º piso pela escada rolante central e vire à direita na Praça de Alimentação.",
            tempo_estimado_min=4,
        ),
        Rota(
            totem_origem_id=1,
            loja_destino_id=7,  # Cinemark (2º Piso)
            url_rota=f"{DEFAULT_MAPPEDIN_URL}&from=totem-1&to=cinemark",
            instrucoes="Suba ao 2º piso e siga até o final da Praça de Alimentação para acessar o Cinemark.",
            tempo_estimado_min=5,
        ),
        # Rotas a partir do Totem 2 (2º Piso - Praça de Alimentação)
        Rota(
            totem_origem_id=2,
            loja_destino_id=1,
            url_rota=f"{DEFAULT_MAPPEDIN_URL}&from=totem-2&to=centauro",
            instrucoes="Desça ao 1º piso pelo elevador central e vire à direita até a Centauro (Loja 104).",
            tempo_estimado_min=4,
        ),
        Rota(
            totem_origem_id=2,
            loja_destino_id=2,
            url_rota=f"{DEFAULT_MAPPEDIN_URL}&from=totem-2&to=riachuelo",
            instrucoes="Desça ao 1º piso pela escada rolante e siga à esquerda até a Riachuelo.",
            tempo_estimado_min=4,
        ),
        Rota(
            totem_origem_id=2,
            loja_destino_id=3,
            url_rota=f"{DEFAULT_MAPPEDIN_URL}&from=totem-2&to=loja-esporte",
            instrucoes="Siga pelo corredor oeste do 2º piso por 60 metros até a Loja Esporte (Loja 205).",
            tempo_estimado_min=2,
        ),
    ]
    db.add_all(rotas_data)
    db.commit()
