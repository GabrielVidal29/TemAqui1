import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{(BASE_DIR / 'temaqui.db').as_posix()}")
if DATABASE_URL.startswith("sqlite:///./"):
    rel_path = DATABASE_URL.replace("sqlite:///./", "")
    DATABASE_URL = f"sqlite:///{(BASE_DIR / rel_path).as_posix()}"

SECRET_KEY = os.getenv("SECRET_KEY", "hackarun-2026-temaqui-capim-dourado-secret")
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]

DEFAULT_MAPPEDIN_URL = "https://app.mappedin.com/map/6af749be2250b6000c4fe524?embedded=true"
