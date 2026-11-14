from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS
from app.database import Base, SessionLocal, engine
from app.routers import lojista, shopping, vitrine
from app.seed import run_seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="TemAqui API — Capim Dourado Shopping (HACKARUN 2026)",
    description=(
        "Plataforma integrada de descoberta de produtos, comparação de ofertas e "
        "navegação indoor 3D (Mappedin) para Totem Interativo, Site Mobile e Painel do Lojista."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if "*" not in CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vitrine.router)
app.include_router(shopping.router)
app.include_router(lojista.router)


@app.get("/", tags=["Health"])
def healthcheck():
    return {
        "status": "ok",
        "sistema": "TemAqui — Capim Dourado Shopping (Palmas, TO)",
        "evento": "HACKARUN 2026",
        "docs": "/docs",
    }
