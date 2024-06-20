from datetime import date, datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    registry,
    relationship,
)

from fast_zero.states import CategoryState, OrderState

table_registry = registry()
Base = declarative_base()


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
    orders: Mapped[list['Order']] = relationship(
        init=False, back_populates='client', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    descricao: Mapped[str]
    valor: Mapped[float]
    codigo_barras: Mapped[str]
    secao: Mapped[str]
    categoria: Mapped[CategoryState]
    estoque_inicial: Mapped[int]
    data_validade: Mapped[date] = mapped_column(nullable=True)
    orders: Mapped[list['Order']] = relationship(
        init=False,
        secondary='order_products',
        back_populates='products',
    )


@table_registry.mapped_as_dataclass
class Order:
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    state: Mapped[OrderState]
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    client: Mapped[Client] = relationship(init=False, back_populates='orders')
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    products: Mapped[list['Product']] = relationship(
        init=False,
        secondary='order_products',
        back_populates='orders',
    )


@table_registry.mapped_as_dataclass
class OrderProduct:
    __tablename__ = 'order_products'

    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id'), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'), primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
