from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import OrderState
from fast_zero.states import CategoryState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ClientSchema(BaseModel):
    nome_completo: str
    email: str
    cpf: str


class ClientPublic(BaseModel):
    id: int
    nome_completo: str
    email: str


class ClientUpdate(BaseModel):
    nome_completo: str | None = None
    email: str | None = None
    cpf: str | None = None


class ClientList(BaseModel):
    clients: list[ClientPublic]


class ProductSchema(BaseModel):
    descricao: str
    valor: float
    codigo_barras: str
    secao: str
    categoria: CategoryState
    estoque_inicial: int
    data_validade: date | None = None


class ProductUpdate(BaseModel):
    descricao: str | None = None
    valor: float | None = None
    codigo_barras: str | None = None
    secao: str | None = None
    categoria: CategoryState | None = None
    estoque_inicial: int | None = None
    data_validade: date | None = None


class ProductPublic(BaseModel):
    id: int
    descricao: str
    valor: float
    codigo_barras: str
    secao: str
    categoria: CategoryState
    estoque_inicial: int
    data_validade: date | None = None


class ProductList(BaseModel):
    products: list[ProductPublic]


class OrderSchema(BaseModel):
    state: OrderState
    client_id: int
    product_ids: list[int]


class OrderUpdate(BaseModel):
    state: OrderState | None = None
    client_id: int | None = None
    product_ids: list[int] | None = None


class OrderPublic(BaseModel):
    id: int
    client_id: int
    state: OrderState


class OrderList(BaseModel):
    orders: list[OrderPublic]


class ProductImage(BaseModel):
    id: int
    file_name: str
    file_type: str


class ProductImageList(BaseModel):
    product_images: list[ProductImage]
