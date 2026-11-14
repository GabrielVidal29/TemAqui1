from fastapi.testclient import TestClient
from app.main import app


def test_rn01_sem_rotas_ecommerce_ou_checkout():
    """RN01: O TemAqui não realiza vendas online, carrinho ou checkout."""
    with TestClient(app) as client:
        openapi = client.get("/openapi.json").json()
        paths = " ".join(openapi.get("paths", {}).keys()).lower()
        assert "carrinho" not in paths
        assert "checkout" not in paths
        assert "pagamento" not in paths


def test_rn02_rn03_rn04_rn09_vitrine_publica_e_produtos_pausados():
    """
    RN02: Vitrine sem login.
    RN03/RN04: Produtos vinculados a lojas com pavimento, localização e mappedin_url.
    RN09: Produtos pausados (ativo=False) não aparecem na vitrine pública.
    """
    with TestClient(app) as client:
        resp = client.get("/api/produtos")
        assert resp.status_code == 200
        produtos = resp.json()
        assert len(produtos) >= 5

        nomes = [p["nome"] for p in produtos]
        # Tênis Urban Sport está pausado no seed (ativo=False)
        assert "Tênis Urban Sport" not in nomes
        assert "Tênis Sprint Run" in nomes

        for p in produtos:
            assert p["ativo"] is True
            assert p["loja"] is not None
            assert p["loja"]["pavimento"] in ("1º Piso", "2º Piso")
            assert "mappedin.com" in p["loja"]["mappedin_url"]
            assert p["atualizado_formatado"].startswith("Atualizado hoje")


def test_rn05_rota_a_partir_da_posicao_fixa_do_totem():
    """
    RN05: Rotas iniciadas no totem devem considerar sempre a posição fixa cadastrada (:totemId).
    """
    with TestClient(app) as client:
        resp_t1 = client.get("/api/rotas?totem_id=1&loja_id=3")
        assert resp_t1.status_code == 200
        data_t1 = resp_t1.json()
        assert data_t1["totem_origem_id"] == 1
        assert data_t1["totem_identificacao"] == "Totem Piso 1"
        assert data_t1["loja_nome"] == "Loja Esporte"
        assert data_t1["tempo_estimado_min"] == 4

        resp_t2 = client.get("/api/rotas?totem_id=2&loja_id=3")
        assert resp_t2.status_code == 200
        data_t2 = resp_t2.json()
        assert data_t2["totem_origem_id"] == 2
        assert data_t2["totem_identificacao"] == "Totem Piso 2"
        assert data_t2["tempo_estimado_min"] == 2


def test_rn06_rn07_rn08_rn09_isolamento_e_gestao_do_lojista():
    """
    RN06/RN07: Atualização de preço/promoção atualiza carimbo comercial.
    RN08: Lojista só visualiza e gerencia produtos da sua própria loja.
    RN09: Pausar produto remove da vitrine pública imediatamente.
    """
    with TestClient(app) as client:
        # Login como Centauro (loja_id=1)
        login_resp = client.post(
            "/api/lojista/login",
            json={"email": "admin@centauro.com.br", "senha": "123456"},
        )
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Listar meus produtos -> todos devem ter loja_id == 1 (RN08)
        meus_resp = client.get("/api/lojista/produtos", headers=headers)
        assert meus_resp.status_code == 200
        meus_produtos = meus_resp.json()
        assert all(p["loja_id"] == 1 for p in meus_produtos)

        # Tentar editar produto id=2 (Riachuelo, loja_id=2) deve retornar 403 Forbidden (RN08)
        forbidden_resp = client.put(
            "/api/lojista/produtos/2",
            json={"preco": 199.90},
            headers=headers,
        )
        assert forbidden_resp.status_code == 403

        # Editar preço promocional do produto id=1 (Centauro) deve funcionar (RN06/RN07)
        update_resp = client.put(
            "/api/lojista/produtos/1",
            json={"preco": 399.90, "preco_promocional": 289.90},
            headers=headers,
        )
        assert update_resp.status_code == 200
        updated = update_resp.json()
        assert updated["preco_final"] == 289.90

        # Restaurar preço original do seed (299.90)
        client.put(
            "/api/lojista/produtos/1",
            json={"preco": 399.90, "preco_promocional": 299.90},
            headers=headers,
        )


def test_lojista_foto_e_exclusao_de_produto():
    """Lojista envia foto (salva no banco), troca a foto e exclui o produto da própria loja."""
    import base64

    png = base64.b64encode(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\rIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa7\x35\x81\x84\x00\x00\x00\x00IEND\xaeB`\x82"
    ).decode()
    with TestClient(app) as client:
        token = client.post(
            "/api/lojista/login", json={"email": "admin@centauro.com.br", "senha": "123456"}
        ).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        novo = client.post(
            "/api/lojista/produtos",
            json={"nome": "Produto Teste Foto", "categoria": "Esportes", "preco": 50},
            headers=headers,
        ).json()
        pid = novo["id"]

        # Formato inválido e conteúdo que não é imagem são recusados
        assert client.put(f"/api/lojista/produtos/{pid}/imagem", json={"imagem": "data:text/plain;base64,aGVsbG8gbXVuZG8gdGVzdGUgdGVzdGU="}, headers=headers).status_code == 422
        assert client.put(f"/api/lojista/produtos/{pid}/imagem", json={"imagem": "data:image/png;base64,aGVsbG8gbXVuZG8gdGVzdGUgdGVzdGU="}, headers=headers).status_code == 422

        # Outra loja não pode trocar a foto (RN08)
        assert client.put("/api/lojista/produtos/2/imagem", json={"imagem": f"data:image/png;base64,{png}"}, headers=headers).status_code == 403

        enviado = client.put(f"/api/lojista/produtos/{pid}/imagem", json={"imagem": f"data:image/png;base64,{png}"}, headers=headers)
        assert enviado.status_code == 200
        url = enviado.json()["imagem_url"]
        assert url.startswith(f"/api/produtos/{pid}/imagem")
        foto = client.get(url)
        assert foto.status_code == 200 and foto.headers["content-type"] == "image/png"

        # Exclusão: outra loja não pode; a própria loja pode, e o produto some da vitrine
        assert client.delete("/api/lojista/produtos/2", headers=headers).status_code == 403
        assert client.delete(f"/api/lojista/produtos/{pid}", headers=headers).status_code == 204
        assert client.get(f"/api/produtos/{pid}").status_code == 404
        assert client.get(f"/api/produtos/{pid}/imagem").status_code == 404
        assert all(p["id"] != pid for p in client.get("/api/lojista/produtos", headers=headers).json())


def test_rota_acessivel_usa_elevador_e_destaca_wc_pcd():
    """Rota 100% acessível: troca escada rolante pelo Elevador Central e destaca o WC PCD."""
    with TestClient(app) as client:
        comum = client.get("/api/rotas?totem_id=1&loja_id=3").json()
        assert comum["acessivel"] is False
        assert any("escadas rolantes" in p.lower() for p in comum["passos"])

        acess = client.get("/api/rotas?totem_id=1&loja_id=3&acessivel=true").json()
        assert acess["acessivel"] is True
        texto = " ".join(acess["passos"]).lower() + " " + acess["instrucoes"].lower()
        assert "escada rolante" not in texto and "escadas rolantes" not in texto
        assert "elevador central" in texto
        assert acess["banheiro_acessivel"] and "WC PCD" in acess["banheiro_acessivel"]
        assert acess["passos"][0].startswith("Você está no Totem Piso 1")
