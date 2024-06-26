from sqlalchemy import select

from fast_zero.models import Client, Order, Product, User


def test_create_user(session):
    new_user = User(
        username='alice', password='secret', email='teste@test', role=''
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user is not None


def test_create_client(session):
    client = Client(
        nome_completo='Jhon Doe',
        cpf='00011122233',
        email='jhondoe@example.com',
    )

    session.add(client)
    session.commit()
    session.refresh(client)

    client = session.scalar(select(Client).where(Client.cpf == '00011122233'))

    assert client is not None


def test_create_product(session):
    product = Product(
        descricao='Tênis AllStar',
        valor=123.45,
        codigo_barras='xxxxxxxxx',
        secao='Vestuário',
        categoria='shoes',
        estoque_inicial=10,
        data_validade=None,
    )

    session.add(product)
    session.commit()
    session.refresh(product)

    product = session.scalar(
        select(Product).where(Product.codigo_barras == 'xxxxxxxxx')
    )

    assert product is not None


def test_create_order(session, client: Client, product: Product):
    order = Order(state='aguardando', client_id=client.id)

    order.products = [product]
    session.add_all([order, product])
    session.commit()
    session.refresh(order)

    client = session.scalar(select(Client).where(Client.id == client.id))
    order = session.scalar(select(Order).where(Order.id == order.id))

    assert order in client.orders
    assert product in order.products
