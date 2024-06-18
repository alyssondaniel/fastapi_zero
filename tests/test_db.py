from sqlalchemy import select

from fast_zero.models import Client, User


def test_create_user(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'


def test_create_client(session, user: User):
    client = Client(
        nome_completo='Jhon Doe',
        cpf='00011122233',
        email='jhondoe@example.com',
    )

    session.add(client)
    session.commit()
    session.refresh(client)

    client = session.scalar(select(Client).where(Client.cpf == '00011122233'))

    assert client.cpf == '00011122233'
