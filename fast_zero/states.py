from enum import Enum


class CategoryState(str, Enum):
    eletronics = 'Eletrônicos'
    clothing = 'roupas'
    shoes = 'calçados'
    books = 'livros'
    games = 'jogos'


class OrderState(str, Enum):
    waiting = 'aguardando'
    paid = 'pago'
    cancel = 'cancelado'
