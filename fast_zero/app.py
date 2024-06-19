from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers import auth, clients, orders, products, users
from fast_zero.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
