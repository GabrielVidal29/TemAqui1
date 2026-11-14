---
description: Workflow /tela que orquestra a execução sequencial PO -> Backend -> Frontend -> QA a cada novo print do Figma enviado pelo usuário.
---

# Workflow `/tela` — Construção Incremental Orientada a Prints do Figma

Use este workflow sempre que o usuário enviar um print de tela do Figma ou solicitar a criação/refinamento de uma tela específica do **TemAqui**.

## Pipeline de Execução Sequencial

### Etapa 1: Product Owner (`.agent/rules/01-po.md`)
1. Leia as diretrizes de `.agent/rules/01-po.md`.
2. Analise minuciosamente a imagem/print anexada pelo usuário (layout, textos, badges, filtros, CTAs, avisos de rodapé e fluxo).
3. Gere a **Task Spec** contendo:
   - Ambiente e rota alvo (`/`, `/totem/:totemId` ou `/lojista`).
   - Requisitos de dados e endpoints de Backend necessários.
   - Componentes e interações de Frontend necessários.
   - Critérios de aceite baseados em `RN01–RN12`.

### Etapa 2: Engenheiro Backend (`.agent/rules/02-backend.md`)
1. Leia as diretrizes de `.agent/rules/02-backend.md`.
2. Atuando **exclusivamente em `backend/`**, implemente ou ajuste:
   - Modelos SQLAlchemy 2.0 (`backend/app/models.py`), se necessário.
   - Schemas Pydantic (`backend/app/schemas.py`).
   - Endpoints FastAPI (`backend/app/routers/`) e dados de `seed.py` para que os produtos, lojas, preços e rotas exibidos no print existam no banco `temaqui.db`.

### Etapa 3: Engenheiro Frontend (`.agent/rules/03-frontend.md`)
1. Leia as diretrizes de `.agent/rules/03-frontend.md`.
2. Atuando **exclusivamente em `frontend/`**, implemente ou refine:
   - Views e componentes em Vue.js 3 fiéis ao print do Figma, utilizando os Design Tokens (`#C9A34A`, `#292929`, `#F5F1E8`, `#FFFFFF`, fonte `Inter`).
   - Integração com a API FastAPI real (`http://localhost:8000`) e com o componente reutilizável `MappedinViewer.vue`.

### Etapa 4: Engenheiro de QA (`.agent/rules/04-qa.md`)
1. Leia as diretrizes de `.agent/rules/04-qa.md`.
2. Execute a suíte de testes automatizados (`pytest`) em `backend/tests/` validando os endpoints e as Regras de Negócio (`RN01–RN12`).
3. Verifique se o servidor Backend (`http://localhost:8000`) e o Frontend (`http://localhost:5173`) estão respondendo corretamente e apresente o resumo executivo da entrega ao usuário.
