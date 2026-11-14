# 📍 TemAqui — Capim Dourado Shopping (HACKARUN 2026)

> **"O que você procura, tem aqui! Encontre. Compare. Vá até a loja."**

O **TemAqui** é uma plataforma integrada de **descoberta de produtos, comparação transparente de ofertas e navegação indoor 3D** desenvolvida para o **Capim Dourado Shopping (Palmas – TO)** durante o **HACKARUN 2026**.

A solução conecta a jornada física do consumidor em três pontos de contato sincronizados em tempo real:
1. **🖥️ Totem Interativo (`1080 × 1920 px`)**: Instalado nos corredores do shopping para descoberta rápida por intenção, orçamento ou ocasião, comparação lado a lado e geração de rota 3D a partir da posição fixa do totem.
2. **📱 Site Mobile Responsivo (`390 × 844 px`)**: Permite iniciar a busca pelo celular ou **continuar exatamente de onde parou no Totem via QR Code**, sem exigir download de aplicativo e sem obrigar cadastro/login.
3. **🏪 Painel Administrativo do Lojista (`1440 × 900 px`)**: Gestão descentralizada para que cada loja do shopping cadastre produtos, atualize preços/promoções e ative ou pause ofertas com reflexo imediato no Totem e no Mobile.

---

## 🎥 Vídeo de Apresentação (Pitch — 90s)

[![Assista ao vídeo de apresentação do TemAqui](https://img.youtube.com/vi/XRJW_cn96EI/hqdefault.jpg)](https://youtu.be/XRJW_cn96EI)

> Clique na imagem acima para assistir à demonstração completa do **TemAqui** no YouTube.
## 🌐 Links de Demonstração Online (Deploy no Render)

Você pode testar todas as interfaces diretamente no navegador pelos links oficiais em produção:

| Ambiente / Interface | Link Direto | Descrição |
| :--- | :--- | :--- |
| 🖥️ **Totem Interativo** | [https://temaqui-web.onrender.com/totem/1](https://temaqui-web.onrender.com/totem/1) | Experiência vertical touch do Totem Piso 1 (Entrada Principal) |
| 📱 **Site Mobile** | [https://temaqui-web.onrender.com/](https://temaqui-web.onrender.com/) | Experiência mobile do consumidor e recepção do QR Code |
| 🏪 **Painel do Lojista** | [https://temaqui-web.onrender.com/lojista](https://temaqui-web.onrender.com/lojista) | Portal administrativo com isolamento por loja |
| 🐈‍⬛ **Easter Egg (Apresentação)** | [https://temaqui-web.onrender.com/totem/1?sexta13](https://temaqui-web.onrender.com/totem/1?sexta13) | Modo Especial **Sexta-Feira 13** com gato preto interativo e cupom `SEXTA13` |
| ⚙️ **API (Swagger / OpenAPI)** | [https://temaqui-api.onrender.com/docs](https://temaqui-api.onrender.com/docs) | Documentação interativa dos endpoints RESTful FastAPI |

> 💡 **Nota sobre o plano gratuito do Render:** Caso o serviço fique inativo por mais de 15 minutos, a primeira requisição pode levar cerca de **30 a 50 segundos** para "acordar" o container da API (`temaqui-api`).

---

## 🧪 Roteiro Passo a Passo: Como Testar o Projeto

### 1. Jornada no Totem Interativo (`/totem/1`)
1. Acesse **[https://temaqui-web.onrender.com/totem/1](https://temaqui-web.onrender.com/totem/1)**.
2. Na **Tela de Boas-Vindas/Descanso**, clique em **"Toque para explorar →"**.
3. **Busca por Orçamento ou Ocasião**:
   - Clique nas sugestões rápidas como **"Tênis até R$ 350"** ou **"Presente para minha mãe"**, ou digite livremente no campo de busca.
4. **Comparador de Ofertas**:
   - Clique em **"Comparar ofertas"** para visualizar lado a lado opções da mesma categoria em diferentes lojas do shopping (preço final, percentual de desconto, piso e tempo de caminhada).
5. **Mapa 3D Interativo (Mappedin) e Rota Fixa**:
   - Clique em **"Como chegar"** em qualquer produto ou loja para abrir o mapa 3D interativo do shopping com a rota traçada a partir da posição fixa do **Totem Piso 1**, seletor de pavimento (`1º Piso` / `2º Piso`) e pontos de interesse (`Elevador`, `Escadas`, `WC`).
6. **Continuidade no Celular via QR Code**:
   - Clique em **"Levar rota no celular (QR Code)"** ou **"Continuar no celular"**.
   - Aponte a câmera do seu smartphone para o **QR Code real** exibido na tela (ou clique sobre o QR Code/botão de simulação) para abrir a jornada diretamente no layout Mobile com a pesquisa e a rota salvas!

---

### 2. Jornada no Site Mobile (`/`)
1. Acesse **[https://temaqui-web.onrender.com/](https://temaqui-web.onrender.com/)** (ou abra pelo QR Code gerado no Totem).
2. Observe que **nenhum login ou cadastro é exigido** (`RN02` / `RN10`). Quando aberto via QR Code do totem, um aviso confirma: *"✓ Pesquisa, comparação e rota do totem salvas"*.
3. Navegue pela barra inferior entre **Início**, **Ofertas**, **Mapa**, **Recompensas** (simulação demonstrativa de vouchers/roleta) e **Perfil**.

---

### 3. Jornada no Painel do Lojista (`/lojista`)
1. Acesse **[https://temaqui-web.onrender.com/lojista](https://temaqui-web.onrender.com/lojista)**.
2. O painel garante **isolamento por loja (`RN08`)**: cada lojista visualiza e gerencia exclusivamente os produtos vinculados à sua loja.
3. Você pode alternar rapidamente entre as contas de demonstração (senha padrão: `123456`):
   - **Centauro (1º Piso):** `admin@centauro.com.br`
   - **Riachuelo (1º Piso):** `admin@riachuelo.com.br`
   - **Loja Esporte (2º Piso):** `admin@lojaesporte.com.br`
   - **Perfumaria (1º Piso):** `admin@perfumaria.com.br`
4. **Teste em Tempo Real**:
   - Clique em **"Editar Preço"** em um produto (ex.: *Tênis Sprint Run*), altere o valor promocional e clique em **"Salvar alterações"**.
   - Ou clique em **"Pausar exibição"** / **"Ativar Promoção"**: produtos pausados deixam imediatamente de aparecer na vitrine pública do Totem e do Mobile (`RN09`).
   - Ou cadastre um **novo produto** e veja-o publicado instantaneamente na vitrine!

---

### 4. 🐈‍⬛ Easter Egg de Apresentação — Modo Sexta-Feira 13 (`?sexta13`)
Desenvolvido especialmente para o hackathon realizado na sexta-feira 13:
1. Acesse **[https://temaqui-web.onrender.com/totem/1?sexta13](https://temaqui-web.onrender.com/totem/1?sexta13)** *(ou dê **13 toques seguidos** na logo `TemAqui` no topo do Totem ou do Mobile)*.
2. Entre na vitrine de ofertas e observe o **gato preto animado** (com olhos dourados e medalhão `13`) passeando entre os cards.
3. **Clique/toque no gato preto** para desbloquear a surpresa **"Sorte de Sexta 13"** com o cupom **`SEXTA13` (13% OFF)** e QR Code exclusivo para resgatar e salvar o cupom no celular!

---

## 🏗️ Arquitetura e Stack Tecnológica

O projeto está estruturado como um **Monorepo** dividido entre Frontend, Backend, Infraestrutura Docker/Render e Governança Multi-Agente:

```text
TemAqui/
├── .agent/                 # Regras e workflows Multi-Agentes (PO, Backend, Frontend e QA)
├── backend/                # API RESTful Python + FastAPI + SQLAlchemy 2 + Pydantic v2
│   ├── app/
│   │   ├── main.py         # Entrypoint FastAPI + CORS + Lifespan (Auto-Seed)
│   │   ├── models.py       # 7 Entidades: Loja, Produto, Promocao, Lojista, Totem, PontoInteresse, Rota
│   │   ├── schemas.py      # Contratos Pydantic e cálculo de descontos/rotas
│   │   ├── seed.py         # População automática idempotente do Capim Dourado Shopping
│   │   └── routers/        # Rotas públicas (vitrine, shopping/mapa) e autenticadas (lojista)
│   ├── tests/              # Testes automatizados Pytest validando as Regras de Negócio (RN01–RN12)
│   └── Dockerfile          # Imagem Python 3.11 de produção
├── frontend/               # Aplicação SPA única em Vue.js 3 + Vite + Vue Router
│   ├── src/
│   │   ├── components/     # MappedinViewer.vue (Mapa 3D), ProductCard, QrCodeModal, Easter Egg Sexta 13
│   │   ├── layouts/        # TotemLayout (1080x1920), MobileLayout (390x844), LojistaLayout (1440x900)
│   │   └── views/          # Telas específicas de cada plataforma consumindo a API real
│   ├── docker/             # Configuração Nginx SPA + injeção dinâmica de runtime (/config.js)
│   └── Dockerfile          # Build multi-stage (Node 20 -> Nginx 1.27 Alpine)
├── docker-compose.yml      # Orquestração completa: PostgreSQL 15 + Backend + Frontend
└── render.yaml             # Blueprint de deploy contínuo no Render
```

---

## 💻 Como Rodar o Projeto Localmente

Você pode executar o projeto de **duas formas**: via **Docker Compose** (com PostgreSQL) ou **Nativamente** (com SQLite, sem precisar de Docker).

### Opção A: Rodando com Docker Compose (Recomendado para Produção/Container)
Na raiz do repositório, execute:

```bash
docker compose up --build
```

Os serviços ficarão disponíveis em:
- **Frontend (Nginx):** `http://localhost:5173`
- **Backend (FastAPI):** `http://localhost:8000` (Swagger em `http://localhost:8000/docs`)
- **Banco de Dados:** PostgreSQL 15 na porta `5432` (populado automaticamente no startup)

---

### Opção B: Rodando Nativamente (Sem Docker — SQLite Automático)

#### 1. Subir o Backend (FastAPI + SQLite)
```bash
cd backend
python -m venv .venv

# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
> Ao iniciar, o backend cria automaticamente o arquivo `backend/temaqui.db` (SQLite) e executa o `seed.py` com as lojas, produtos, promoções, totens, POIs e rotas do Capim Dourado Shopping.

#### 2. Subir o Frontend (Vue.js 3 + Vite)
Em outro terminal:
```bash
cd frontend
npm install
npm run dev
```
Acesse em **`http://localhost:5173`**.

---

### ✅ Executando os Testes Automatizados (QA)
Para validar automaticamente as Regras de Negócio (`RN01` a `RN12` — ausência de checkout online, vitrine sem login, rotas fixas por totem, atualização comercial, isolamento de lojista e ocultação de produtos pausados):

```bash
cd backend
pytest tests/test_regras_negocio.py -v
```
