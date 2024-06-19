from datetime import date, datetime
from enum import Enum

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


class Category(str, Enum):
    eletronics = 'Eletrônicos'
    clothing = 'roupas'
    shoes = 'calçados'
    books = 'livros'
    games = 'jogos'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class Client:
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome_completo: Mapped[str]
    cpf: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    descricao: Mapped[str]
    valor: Mapped[float]
    codigo_barras: Mapped[str]
    secao: Mapped[str]
    categoria: Mapped[Category]
    estoque_inicial: Mapped[int]
    data_validade: Mapped[date] = mapped_column(nullable=True)
