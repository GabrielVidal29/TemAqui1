"""
Motor de busca da vitrine do TemAqui.

Interpreta a frase digitada no totem/celular (ex.: "tênis de corrida até R$ 350",
"presente para minha mãe") e devolve filtros estruturados + função de relevância.
Sem dependências externas: normalização de acentos, stopwords, sinônimos e ocasiões.
"""
import re
import unicodedata
from dataclasses import dataclass, field
from typing import List, Optional, Set


def normalizar(texto: Optional[str]) -> str:
    if not texto:
        return ""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return sem_acento.lower()


STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas", "de", "da", "do", "das", "dos", "e", "ou",
    "em", "no", "na", "nos", "nas", "para", "pra", "pro", "por", "com", "sem", "que", "ate",
    "meu", "minha", "meus", "minhas", "seu", "sua", "quero", "procuro", "procurando", "algo",
    "r", "rs", "reais", "real", "preco", "barato", "barata", "baratos", "loja", "lojas",
}

# Palavra digitada -> alternativas que contam como correspondência (já normalizadas)
SINONIMOS = {
    "tenis": ["tenis", "calcado"],
    "calcado": ["calcado", "tenis", "sapato"],
    "sapato": ["sapato", "calcado", "tenis"],
    "corrida": ["corrida", "running", "tenis", "esport"],
    "correr": ["corrida", "running", "tenis", "esport"],
    "academia": ["academia", "treino", "esport"],
    "treino": ["treino", "academia", "esport"],
    "roupa": ["moda", "camiseta", "calca", "vestido", "blusa", "jaqueta", "bermuda"],
    "roupas": ["moda", "camiseta", "calca", "vestido", "blusa", "jaqueta", "bermuda"],
    "comida": ["alimentacao", "restaurante"],
    "comer": ["alimentacao", "restaurante"],
    "almoco": ["almoco", "alimentacao", "restaurante"],
    "jantar": ["alimentacao", "restaurante"],
    "restaurante": ["restaurante", "alimentacao"],
    "cinema": ["cinema", "ingresso", "pipoca", "lazer", "cinemark"],
    "filme": ["cinema", "ingresso", "lazer", "cinemark"],
    "livro": ["livro", "livraria", "literatura"],
    "ler": ["livro", "livraria", "literatura"],
    "brinquedo": ["brinquedo", "jogo", "pelucia"],
    "perfume": ["perfume", "perfumaria", "fragrancia", "body splash"],
    "beleza": ["perfumaria", "hidratante", "perfume", "creme"],
    "bolsa": ["bolsa", "mochila", "carteira"],
    "relogio": ["relogio"],
    "oculos": ["oculos"],
    "jeans": ["jeans"],
}

# Ocasiões de presente: palavras -> categorias sugeridas
OCASIOES = [
    ({"mae", "mamae", "esposa", "namorada", "ela", "avo", "irma", "amiga", "tia", "sogra"},
     ["Perfumaria", "Moda", "Acessórios", "Livros"]),
    ({"pai", "papai", "marido", "namorado", "ele", "irmao", "amigo", "tio", "sogro"},
     ["Perfumaria", "Acessórios", "Esportes", "Livros"]),
    ({"crianca", "criancas", "filho", "filha", "sobrinho", "sobrinha", "infantil", "menino",
      "menina", "bebe", "neto", "neta"},
     ["Brinquedos", "Livros"]),
]
CATEGORIAS_PRESENTE_PADRAO = ["Perfumaria", "Acessórios", "Livros", "Brinquedos", "Moda"]

PRECO_RE = re.compile(
    r"(?:ate|abaixo de|menos de|no maximo|maximo|max|por ate)\s*(?:r\s*\$)?\s*(\d+(?:[.,]\d{1,2})?)"
)


@dataclass
class ConsultaInterpretada:
    termos: List[List[str]] = field(default_factory=list)  # cada termo = lista de alternativas
    preco_max: Optional[float] = None
    categorias_ocasiao: List[str] = field(default_factory=list)
    eh_presente: bool = False


def _singular(token: str) -> str:
    if len(token) > 4 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def interpretar(q: Optional[str]) -> ConsultaInterpretada:
    consulta = ConsultaInterpretada()
    texto = normalizar(q).strip()
    if not texto:
        return consulta

    m = PRECO_RE.search(texto)
    if m:
        consulta.preco_max = float(m.group(1).replace(",", "."))
        texto = texto[: m.start()] + " " + texto[m.end():]

    tokens = [t for t in re.split(r"[^a-z0-9&]+", texto) if t]
    palavras_ocasiao: Set[str] = set()

    if any(t.startswith("presente") or t == "presentear" for t in tokens):
        consulta.eh_presente = True
        for gatilhos, categorias in OCASIOES:
            if gatilhos.intersection(tokens):
                palavras_ocasiao |= gatilhos
                for c in categorias:
                    if c not in consulta.categorias_ocasiao:
                        consulta.categorias_ocasiao.append(c)
        if not consulta.categorias_ocasiao:
            consulta.categorias_ocasiao = list(CATEGORIAS_PRESENTE_PADRAO)

    for token in tokens:
        if token in STOPWORDS or token.isdigit() or token in palavras_ocasiao:
            continue
        if token.startswith("presente") or token == "presentear":
            continue
        base = _singular(token)
        alternativas = SINONIMOS.get(token) or SINONIMOS.get(base) or [base]
        consulta.termos.append(alternativas)

    return consulta


def pontuar(alternativas: List[str], campos: dict) -> int:
    """Pontua um termo nos campos do produto (nome pesa mais que descrição)."""
    pesos = {"nome": 4, "categoria": 3, "loja": 3, "loja_categoria": 2, "descricao": 1}
    melhor = 0
    for alt in alternativas:
        for campo, peso in pesos.items():
            if alt in campos[campo]:
                melhor = max(melhor, peso)
    return melhor
