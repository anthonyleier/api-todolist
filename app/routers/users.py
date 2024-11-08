from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.schemas import FilterPage, Message, UserList, UserPublic, UserSchema
from app.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
DatabaseSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: DatabaseSession):
    db_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Username already exists')
        elif db_user.email == user.email:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Email already exists')

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password, email=user.email)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(session: DatabaseSession, filter_users: Annotated[FilterPage, Query()]):
    users = session.scalars(select(User).offset(filter_users.offset).limit(filter_users.limit)).all()
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: DatabaseSession):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: DatabaseSession, current_user: CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email

        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Username or email already exists')


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: DatabaseSession, current_user: CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}