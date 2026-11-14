import base64
import hashlib
import hmac
import json
from typing import Optional
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.config import SECRET_KEY
from app.database import get_db
from app.models import Lojista


def hash_password(password: str) -> str:
    return hashlib.sha256(f"{SECRET_KEY}:{password}".encode("utf-8")).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_password(password), hashed)


def create_access_token(lojista_id: int, loja_id: int, email: str) -> str:
    payload = {"lojista_id": lojista_id, "loja_id": loja_id, "email": email}
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    b64 = base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")
    sig = hmac.new(SECRET_KEY.encode("utf-8"), b64.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{b64}.{sig}"


def decode_access_token(token: str) -> dict:
    try:
        b64, sig = token.split(".", 1)
        expected_sig = hmac.new(
            SECRET_KEY.encode("utf-8"), b64.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            raise ValueError("Invalid token signature")
        padding = "=" * (-len(b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(b64 + padding).decode("utf-8"))
        return payload
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido ou expirado.",
        ) from exc


def get_current_lojista(
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
) -> Lojista:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação obrigatória para acessar o Portal do Lojista.",
        )
    token = authorization.split(" ", 1)[1].strip()
    payload = decode_access_token(token)
    lojista = db.query(Lojista).filter(Lojista.id == payload.get("lojista_id")).first()
    if not lojista:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Lojista não encontrado.",
        )
    return lojista
