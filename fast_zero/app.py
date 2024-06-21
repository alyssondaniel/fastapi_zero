from http import HTTPStatus

import sentry_sdk
from fastapi import FastAPI

from fast_zero.routers import auth, clients, orders, products, users
from fast_zero.schemas import Message
from fast_zero.security import settings

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get('/sentry-debug')
async def trigger_error():
    division_by_zero = 1 / 0


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
