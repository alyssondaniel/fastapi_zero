from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_zero.security import (
    RoleChecker,
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['users'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(
    user: UserSchema,
    session: Session,
    _: Annotated[bool, Depends(RoleChecker(allowed_roles=['admin']))],
):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        password=hashed_password,
        email=user.email,
        role=user.role,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def list_users(
    _: Annotated[bool, Depends(RoleChecker(allowed_roles=['admin']))],
    session: Session,
    skip: int = 0,
    limit: int = 100,
):
    users = session.scalars(
        select(User).where(User.role == 'guest').offset(skip).limit(limit)
    ).all()
    return {'users': users}


@router.get('/{id}', response_model=UserPublic)
def show_user(
    _: Annotated[bool, Depends(RoleChecker(allowed_roles=['admin']))],
    id: int,
    session: Session,
):
    user: User = session.scalars(select(User).filter(User.id == id)).first()

    return user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    _: Annotated[bool, Depends(RoleChecker(allowed_roles=['admin']))],
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    db_user.username = user.username
    db_user.password = get_password_hash(user.password)
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)

    return db_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    _: Annotated[bool, Depends(RoleChecker(allowed_roles=['admin']))],
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
