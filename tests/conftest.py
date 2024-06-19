import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.factories import (
    ClientFactory,
    OrderFactory,
    ProductFactory,
    UserFactory,
)
from fast_zero.models import table_registry
from fast_zero.security import get_password_hash


@pytest.fixture()
def clientHttp(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
        # echo=True,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture()
def client(session):
    client = ClientFactory()

    session.add(client)
    session.commit()
    session.refresh(client)

    return client


@pytest.fixture()
def products(session):
    products = ProductFactory.create_batch(3)
    session.add_all(products)
    session.commit()
    # session.refresh(products)

    return products


@pytest.fixture()
def product(session):
    product = ProductFactory(secao='alimentacao')

    session.add(product)
    session.commit()
    session.refresh(product)

    return product


@pytest.fixture()
def order(session):
    order = OrderFactory()

    session.add(order)
    session.commit()
    session.refresh(order)

    return order


@pytest.fixture()
def user_other(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture()
def token(clientHttp, user):
    response = clientHttp.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
