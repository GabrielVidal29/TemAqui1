"""
Catálogo ampliado de demonstração (HACKARUN 2026).

Simula o sistema em funcionamento real: várias lojas do Capim Dourado Shopping, cada uma com
diversos produtos cadastrados pelo lojista (com e sem promoção, alguns pausados).

É idempotente e aditivo: roda depois do seed base e só insere o que ainda não existe
(lojas por id, produtos por nome + loja, lojistas por e-mail). Assim, bancos já criados
recebem o catálogo novo sem perder dados nem quebrar os IDs usados nos testes.
"""
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.auth import hash_password
from app.config import DEFAULT_MAPPEDIN_URL
from app.fotos_produtos import FOTOS_PRODUTOS
from app.models import Loja, Lojista, Produto, ProdutoExcluido, Promocao

IMG = "/assets/products"

# Categoria de vitrine de cada loja (as lojas 1–7 já existem no seed base)
CATEGORIA_LOJAS = {
    1: "Esportes",
    2: "Moda",
    3: "Esportes",
    4: "Perfumaria",
    5: "Acessórios",
    6: "Restaurantes",
    7: "Lazer",
}

NOVAS_LOJAS = [
    {
        "id": 8,
        "nome": "Renner",
        "descricao": "Moda feminina, masculina e infantil, com coleções da estação e básicos para o dia a dia.",
        "categoria": "Moda",
        "pavimento": "1º Piso",
        "slug": "renner",
        "localizacao": "1º Pavimento • Loja Âncora Oeste",
    },
    {
        "id": 9,
        "nome": "C&A",
        "descricao": "Moda acessível para toda a família, jeans, malharia e acessórios.",
        "categoria": "Moda",
        "pavimento": "1º Piso",
        "slug": "cea",
        "localizacao": "1º Pavimento • Loja 130",
    },
    {
        "id": 10,
        "nome": "Leitura",
        "descricao": "Livraria com best-sellers, literatura infantil, papelaria e presentes.",
        "categoria": "Livraria",
        "pavimento": "1º Piso",
        "slug": "leitura",
        "localizacao": "1º Pavimento • Loja 140",
    },
    {
        "id": 11,
        "nome": "Ri Happy",
        "descricao": "Brinquedos, jogos e presentes para todas as idades.",
        "categoria": "Brinquedos",
        "pavimento": "2º Piso",
        "slug": "ri-happy",
        "localizacao": "2º Pavimento • Loja 230",
    },
]

# (nome, categoria, preco, preco_promocional | None, imagem, descricao, ativo)
PRODUTOS_POR_LOJA = {
    1: [  # Centauro
        ("Camiseta Dry Fit Treino", "Esportes", 89.90, 69.90, "camiseta-grafite",
         "Tecido leve de secagem rápida para treinos e corrida. Tamanhos P ao GG.", True),
        ("Bermuda Running Leve", "Esportes", 119.90, None, "bermuda",
         "Bermuda com bolso para celular e tecido respirável para corrida.", True),
        ("Garrafa Squeeze 750 ml", "Esportes", 49.90, 39.90, "garrafa",
         "Garrafa livre de BPA com bico antivazamento. Ideal para academia e corrida.", True),
        ("Mochila Esportiva 25 L", "Esportes", 229.90, 179.90, "mochila",
         "Compartimento para tênis, bolso térmico e alças acolchoadas.", True),
        ("Jaqueta Corta-Vento", "Esportes", 299.90, 249.90, "corta-vento",
         "Corta-vento leve e dobrável com faixa refletiva para corrida noturna.", True),
        ("Boné Performance", "Esportes", 79.90, None, "bone",
         "Boné com aba curva, tecido tecnológico e regulagem traseira.", True),
    ],
    2: [  # Riachuelo
        ("Vestido Midi Floral", "Moda", 189.90, 149.90, "vestido-floral",
         "Vestido midi em viscose com estampa floral. Ótima opção de presente.", True),
        ("Calça Jeans Slim", "Moda", 159.90, None, "calca-jeans",
         "Jeans com elastano, modelagem slim e lavagem média.", True),
        ("Camiseta Básica Algodão", "Moda", 39.90, None, "camiseta-branca",
         "Camiseta 100% algodão, gola careca. Várias cores disponíveis na loja.", True),
        ("Jaqueta Jeans Clássica", "Moda", 229.90, 179.90, "jaqueta",
         "Jaqueta jeans com botões metálicos e bolsos frontais.", True),
        ("Blusa Feminina Rosé", "Moda", 79.90, 59.90, "camiseta-rosa",
         "Blusa em malha macia na cor rosé, caimento solto.", True),
        ("Bolsa Transversal Caramelo", "Acessórios", 129.90, None, "bolsa-caramelo",
         "Bolsa transversal compacta com alça regulável.", True),
    ],
    3: [  # Loja Esporte
        ("Tênis Trail Pro", "Calçados", 499.90, 429.90, "tenis-move",
         "Tênis de corrida em trilha com solado de alta aderência e proteção na biqueira.", True),
        ("Relógio Esportivo GPS", "Esportes", 899.90, 749.90, "relogio-esportivo",
         "GPS integrado, monitor cardíaco e mais de 20 modos esportivos. Ideal para corrida.", True),
        ("Mochila Trilha 30 L", "Esportes", 349.90, None, "mochila-trilha",
         "Mochila para trilha com capa de chuva, costas ventiladas e porta-hidratação.", True),
        ("Garrafa Térmica 1 L", "Esportes", 139.90, 109.90, "garrafa",
         "Mantém a bebida gelada por 24h. Aço inox com tampa esportiva.", True),
        ("Camiseta Proteção UV", "Esportes", 119.90, None, "camiseta-grafite",
         "Camiseta com proteção UV50+ para corrida e atividades ao ar livre.", True),
        ("Boné Trail", "Esportes", 69.90, 54.90, "bone",
         "Boné leve com tela respirável e proteção solar.", True),
    ],
    4: [  # Perfumaria
        ("Perfume Floral Rosé 75 ml", "Perfumaria", 289.90, 229.90, "perfume-rose",
         "Fragrância floral com notas de rosa e peônia. Um presente delicado para mãe ou namorada.", True),
        ("Perfume Bosque Masculino 100 ml", "Perfumaria", 319.90, None, "perfume-amadeirado",
         "Fragrância amadeirada intensa com notas de cedro e vetiver. Presente para pai.", True),
        ("Body Splash Floral 200 ml", "Perfumaria", 69.90, None, "perfume-rose",
         "Body splash refrescante para o dia a dia.", True),
        ("Hidratante Corporal 400 ml", "Perfumaria", 59.90, 44.90, "hidratante",
         "Hidratação por 48h com manteiga de karité e óleo de amêndoas.", True),
        ("Kit Presente Essencial", "Perfumaria", 349.90, 279.90, "perfume-essencial",
         "Perfume Essencial 50 ml + hidratante + necessaire. Embalagem para presente inclusa.", True),
        ("Creme para Mãos 75 g", "Perfumaria", 39.90, None, "hidratante",
         "Creme de rápida absorção com fragrância suave.", False),
    ],
    5: [  # Acessórios
        ("Carteira Couro Slim", "Acessórios", 149.90, 119.90, "carteira",
         "Carteira compacta em couro legítimo com porta-cartões. Presente para pai.", True),
        ("Óculos de Sol Aviador", "Acessórios", 249.90, 199.90, "oculos",
         "Lentes polarizadas com proteção UV400 e armação dourada.", True),
        ("Relógio Clássico Dourado", "Acessórios", 459.90, None, "relogio-dourado",
         "Relógio analógico com caixa dourada e pulseira em couro. Presente elegante.", True),
        ("Mochila Executiva", "Acessórios", 299.90, 239.90, "mochila",
         "Compartimento para notebook de 15,6\" e porta USB.", True),
        ("Cinto Couro Legítimo", "Acessórios", 99.90, None, "cinto",
         "Cinto em couro com fivela dourada.", True),
    ],
    6: [  # Outback
        ("Costela Barbecue", "Alimentação", 129.90, 109.90, "prato-costela",
         "Costela suína com molho barbecue e acompanhamento. Promoção válida no almoço de segunda a sexta.", True),
        ("Hambúrguer da Casa", "Alimentação", 69.90, None, "hamburguer",
         "Blend bovino de 180 g, queijo cheddar, bacon e fritas.", True),
        ("Almoço Executivo", "Alimentação", 59.90, 49.90, "prato-executivo",
         "Prato principal + acompanhamento + bebida, de segunda a sexta até 15h.", True),
        ("Picanha Grelhada", "Alimentação", 99.90, None, "prato-executivo",
         "Picanha grelhada com arroz, farofa e vinagrete.", True),
    ],
    7: [  # Cinemark
        ("Ingresso Sala 2D", "Lazer", 32.00, None, "ingresso",
         "Ingresso inteira para sessões 2D. Meia-entrada mediante comprovação na bilheteria.", True),
        ("Ingresso Sala XD", "Lazer", 46.00, 36.00, "ingresso",
         "Tela gigante e som imersivo. Preço promocional às terças-feiras.", True),
        ("Combo Pipoca Grande + 2 Refris", "Alimentação", 59.90, 49.90, "pipoca",
         "Pipoca grande e dois refrigerantes de 500 ml.", True),
        ("Pipoca Média", "Alimentação", 28.90, None, "pipoca",
         "Pipoca média salgada ou doce.", True),
    ],
    8: [  # Renner
        ("Vestido Longo Estampado", "Moda", 219.90, 169.90, "vestido-floral",
         "Vestido longo com estampa floral e alças finas.", True),
        ("Jaqueta Couro Sintético", "Moda", 299.90, None, "jaqueta",
         "Jaqueta em couro sintético com zíper frontal.", True),
        ("Calça Jeans Reta", "Moda", 179.90, 139.90, "calca-jeans",
         "Calça jeans de modelagem reta e cintura alta.", True),
        ("Camiseta Estampada", "Moda", 59.90, None, "camiseta-grafite",
         "Camiseta em algodão com estampa exclusiva.", True),
        ("Óculos de Sol Gatinho", "Acessórios", 129.90, 99.90, "oculos",
         "Óculos com armação gatinho e lentes com proteção UV.", True),
        ("Tênis Casual Branco", "Calçados", 199.90, 159.90, "tenis-urban",
         "Tênis casual em material sintético, combina com tudo.", True),
    ],
    9: [  # C&A
        ("Camiseta Básica Pack 3", "Moda", 79.90, 59.90, "camiseta-branca",
         "Kit com 3 camisetas básicas de algodão.", True),
        ("Calça Jogger Jeans", "Moda", 139.90, None, "calca-jeans",
         "Calça jogger em jeans com elástico na barra.", True),
        ("Blusa Tricô Rosé", "Moda", 99.90, 79.90, "camiseta-rosa",
         "Blusa de tricô leve, ideal para meia-estação.", True),
        ("Bermuda Sarja", "Moda", 89.90, None, "bermuda",
         "Bermuda em sarja com elastano.", True),
        ("Tênis Casual Conforto", "Calçados", 149.90, 119.90, "tenis-move",
         "Tênis leve com palmilha macia para o dia a dia.", True),
    ],
    10: [  # Leitura
        ("Box Clássicos da Literatura", "Livros", 189.90, 149.90, "box-livros",
         "Box com 4 clássicos da literatura brasileira. Ótima ideia de presente.", True),
        ("Livro de Receitas do Cerrado", "Livros", 89.90, None, "livro",
         "Receitas regionais do Tocantins e do Cerrado, com fotos.", True),
        ("Romance Best-seller", "Livros", 59.90, 47.90, "livro",
         "Romance mais vendido da semana. Presente para mãe que ama ler.", True),
        ("Agenda 2027", "Livros", 69.90, 54.90, "agenda",
         "Agenda diária com capa dura e marcador de página.", True),
        ("Livro Infantil Ilustrado", "Livros", 49.90, None, "livro",
         "Livro ilustrado para crianças de 4 a 8 anos.", True),
    ],
    11: [  # Ri Happy
        ("Blocos de Montar 500 Peças", "Brinquedos", 199.90, 159.90, "blocos",
         "Blocos de montar compatíveis com as principais marcas. A partir de 6 anos.", True),
        ("Urso de Pelúcia 40 cm", "Brinquedos", 129.90, None, "urso",
         "Pelúcia antialérgica e super macia. Presente para crianças.", True),
        ("Jogo de Tabuleiro Família", "Brinquedos", 149.90, 119.90, "jogo-tabuleiro",
         "Jogo para 2 a 6 jogadores, diversão para toda a família.", True),
        ("Carrinho de Controle Remoto", "Brinquedos", 249.90, None, "carrinho",
         "Carrinho recarregável com controle de longo alcance.", True),
    ],
}

NOVOS_LOJISTAS = [
    (5, "Acessórios • Administrador", "admin@acessorios.com.br"),
    (6, "Outback • Administrador", "admin@outback.com.br"),
    (7, "Cinemark • Administrador", "admin@cinemark.com.br"),
    (8, "Renner • Administrador", "admin@renner.com.br"),
    (9, "C&A • Administrador", "admin@cea.com.br"),
    (10, "Leitura • Administrador", "admin@leitura.com.br"),
    (11, "Ri Happy • Administrador", "admin@rihappy.com.br"),
]


def _sincronizar_sequencias_postgres(db: Session) -> None:
    """No PostgreSQL, inserts com id explícito (seed base) não avançam a sequence da tabela."""
    if db.get_bind().dialect.name != "postgresql":
        return
    for tabela in ("lojas", "produtos", "promocoes", "lojistas"):
        db.execute(
            text(
                f"SELECT setval(pg_get_serial_sequence('{tabela}', 'id'), "
                f"COALESCE((SELECT MAX(id) FROM {tabela}), 1))"
            )
        )


def run_seed_catalogo(db: Session) -> None:
    _sincronizar_sequencias_postgres(db)
    base_time = datetime.now().replace(hour=10, minute=42, second=0, microsecond=0)
    fim_promo = base_time + timedelta(days=7)

    # 1. Categorias de vitrine das lojas existentes
    for loja_id, categoria in CATEGORIA_LOJAS.items():
        loja = db.get(Loja, loja_id)
        if loja and loja.categoria != categoria:
            loja.categoria = categoria

    # 2. Novas lojas
    for spec in NOVAS_LOJAS:
        if db.get(Loja, spec["id"]) is None:
            db.add(
                Loja(
                    id=spec["id"],
                    nome=spec["nome"],
                    descricao=spec["descricao"],
                    categoria=spec["categoria"],
                    pavimento=spec["pavimento"],
                    mappedin_url=f"{DEFAULT_MAPPEDIN_URL}&store={spec['slug']}",
                    localizacao=spec["localizacao"],
                )
            )
    db.flush()

    # 3. Produtos de cada loja (com horários de atualização variados ao longo da manhã)
    existentes = {(p.nome, p.loja_id) for p in db.query(Produto.nome, Produto.loja_id).all()}
    # Produtos que o lojista excluiu não voltam a ser criados
    existentes |= {(e.nome, e.loja_id) for e in db.query(ProdutoExcluido.nome, ProdutoExcluido.loja_id).all()}
    minuto = 0
    for loja_id, produtos in PRODUTOS_POR_LOJA.items():
        for nome, categoria, preco, promo, imagem, descricao, ativo in produtos:
            minuto += 7
            if (nome, loja_id) in existentes:
                continue
            atualizado = base_time - timedelta(minutes=minuto % 150)
            prod = Produto(
                nome=nome,
                descricao=descricao,
                categoria=categoria,
                preco=preco,
                imagem_url=f"{IMG}/{imagem}.svg",
                ativo=ativo,
                atualizado_em=atualizado,
                loja_id=loja_id,
            )
            db.add(prod)
            db.flush()
            if promo is not None:
                db.add(
                    Promocao(
                        produto_id=prod.id,
                        preco_promocional=promo,
                        data_inicio=atualizado - timedelta(days=1),
                        data_fim=fim_promo,
                        ativa=True,
                    )
                )

    # 4. Lojistas das demais lojas (senha demo 123456)
    emails = {e for (e,) in db.query(Lojista.email).all()}
    for loja_id, nome, email in NOVOS_LOJISTAS:
        if email not in emails:
            db.add(Lojista(nome=nome, email=email, senha_hash=hash_password("123456"), loja_id=loja_id))

    # 5. Fotos reais dos produtos (troca só as ilustrações padrão, nunca uma imagem escolhida pelo lojista)
    db.flush()
    for prod in db.query(Produto).all():
        foto = FOTOS_PRODUTOS.get(prod.nome)
        if foto and prod.imagem_url.startswith(f"{IMG}/") and prod.imagem_url.endswith(".svg"):
            prod.imagem_url = f"{IMG}/fotos/{foto}"

    db.commit()
