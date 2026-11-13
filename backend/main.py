
from fastapi import FastAPI

app = FastAPI(title="TemAqui API")

@app.get("/")
def inicio():
    return {"mensagem": "Bem-vindo ao TemAqui!"}
