from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Client, User
from fast_zero.schemas import ClientList, ClientPublic, ClientSchema, Message
from fast_zero.security import get_current_user

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/clients', tags=['clients'])


@router.post('/', response_model=ClientPublic)
def create_client(
    client: ClientSchema,
    session: Session,
    current_user: CurrentUser = None,
):
    db_client: Client = Client(
        nome_completo=client.nome_completo,
        cpf=client.cpf,
        email=client.email,
    )
    session.add(db_client)
    session.commit()
    session.refresh(db_client)

    return db_client


@router.get('/', response_model=ClientList)
def list_clients(  # noqa
    session: Session,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
    current_user: CurrentUser = None,
):
    query = select(Client)

    if title:
        query = query.filter(Client.title.contains(title))

    if description:
        query = query.filter(Client.description.contains(description))

    if state:
        query = query.filter(Client.state == state)

    clients = session.scalars(query.offset(offset).limit(limit)).all()

    return {'clients': clients}


@router.put('/{client_id}', response_model=ClientPublic)
def update_client(client_id: int, session: Session, client: ClientSchema):
    db_client = session.scalar(select(Client).where(Client.id == client_id))

    if not db_client:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Client not found.'
        )

    for key, value in client.model_dump(exclude_unset=True).items():
        setattr(db_client, key, value)

    session.add(db_client)
    session.commit()
    session.refresh(db_client)

    return db_client


@router.delete('/{client_id}', response_model=Message)
def delete_client(
    client_id: int,
    session: Session,
    current_user: CurrentUser = None,
):
    client = session.scalar(select(Client).where(Client.id == client_id))

    if not client:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Client not found.'
        )

    session.delete(client)
    session.commit()

    return {'message': 'Client has been deleted successfully.'}
