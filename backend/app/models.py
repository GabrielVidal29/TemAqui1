from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, LargeBinary, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Loja(Base):
    __tablename__ = "lojas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    categoria: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    pavimento: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    mappedin_url: Mapped[str] = mapped_column(String(500), nullable=False)
    localizacao: Mapped[str] = mapped_column(String(120), nullable=False)

    produtos: Mapped[List["Produto"]] = relationship(
        "Produto", back_populates="loja", cascade="all, delete-orphan"
    )
    lojistas: Mapped[List["Lojista"]] = relationship(
        "Lojista", back_populates="loja", cascade="all, delete-orphan"
    )
    rotas: Mapped[List["Rota"]] = relationship(
        "Rota", back_populates="loja_destino", cascade="all, delete-orphan"
    )


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    categoria: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    imagem_url: Mapped[str] = mapped_column(String(500), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    loja_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lojas.id", ondelete="CASCADE"), nullable=False, index=True
    )

    loja: Mapped["Loja"] = relationship("Loja", back_populates="produtos")
    promocoes: Mapped[List["Promocao"]] = relationship(
        "Promocao", back_populates="produto", cascade="all, delete-orphan"
    )
    imagem: Mapped[Optional["ImagemProduto"]] = relationship(
        "ImagemProduto", back_populates="produto", cascade="all, delete-orphan", uselist=False
    )


class ImagemProduto(Base):
    """
    Foto enviada pelo lojista. Fica no próprio banco (e não em disco) porque o disco
    dos serviços gratuitos do Render é apagado a cada reinício/deploy.
    """
    __tablename__ = "imagens_produto"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    produto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    mime: Mapped[str] = mapped_column(String(40), nullable=False)
    conteudo: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    produto: Mapped["Produto"] = relationship("Produto", back_populates="imagem")


class ProdutoExcluido(Base):
    """
    Registro dos produtos excluídos pelo lojista, para que o catálogo de demonstração
    (seed_catalogo) não os recrie quando o servidor reiniciar.
    """
    __tablename__ = "produtos_excluidos"
    __table_args__ = (UniqueConstraint("nome", "loja_id", name="uq_produto_excluido"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(160), nullable=False)
    loja_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    excluido_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)


class Promocao(Base):
    __tablename__ = "promocoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    produto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    preco_promocional: Mapped[float] = mapped_column(Float, nullable=False)
    data_inicio: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    data_fim: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)

    produto: Mapped["Produto"] = relationship("Produto", back_populates="promocoes")


class Lojista(Base):
    __tablename__ = "lojistas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(160), unique=True, nullable=False, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    loja_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lojas.id", ondelete="CASCADE"), nullable=False, index=True
    )

    loja: Mapped["Loja"] = relationship("Loja", back_populates="lojistas")


class Totem(Base):
    __tablename__ = "totens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    identificacao: Mapped[str] = mapped_column(String(100), nullable=False)
    pavimento: Mapped[str] = mapped_column(String(40), nullable=False)
    posicao_referencia: Mapped[str] = mapped_column(String(160), nullable=False)

    rotas: Mapped[List["Rota"]] = relationship(
        "Rota", back_populates="totem_origem", cascade="all, delete-orphan"
    )


class PontoInteresse(Base):
    __tablename__ = "pontos_interesse"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(
        String(40), nullable=False, index=True
    )  # banheiro, elevador, saida, alimentacao, escada
    pavimento: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    localizacao: Mapped[str] = mapped_column(String(160), nullable=False)


class Rota(Base):
    __tablename__ = "rotas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    totem_origem_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("totens.id", ondelete="CASCADE"), nullable=False, index=True
    )
    loja_destino_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lojas.id", ondelete="CASCADE"), nullable=False, index=True
    )
    url_rota: Mapped[str] = mapped_column(String(500), nullable=False)
    instrucoes: Mapped[str] = mapped_column(Text, nullable=False)
    tempo_estimado_min: Mapped[int] = mapped_column(Integer, nullable=False, default=2)

    totem_origem: Mapped["Totem"] = relationship("Totem", back_populates="rotas")
    loja_destino: Mapped["Loja"] = relationship("Loja", back_populates="rotas")
