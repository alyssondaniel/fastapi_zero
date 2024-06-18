from pydantic import BaseModel, ConfigDict, EmailStr


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


class ClientList(BaseModel):
    clients: list[ClientPublic]
