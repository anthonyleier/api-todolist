from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Todo, User
from app.schemas import FilterTodo, TodoList, TodoPublic, TodoSchema, TodoUpdate
from app.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])
DatabaseSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, user: CurrentUser, session: DatabaseSession):
    db_todo = Todo(todo.title, todo.description, todo.state, user_id=user.id)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
def read_todos(session: DatabaseSession, user: CurrentUser, filter_todos: Annotated[FilterTodo, Query()]):
    query = select(Todo).where(Todo.user_id == user.id)

    if filter_todos.title:
        query = query.filter(Todo.title.contains(filter_todos.title))

    if filter_todos.description:
        query = query.filter(Todo.description.contains(filter_todos.description))

    if filter_todos.state:
        query = query.filter(Todo.state == filter_todos.state)

    todos = session.scalars(query.offset(filter_todos.offset).limit(filter_todos.limit)).all()
    return {'todos': todos}


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(todo_id: int, session: DatabaseSession, user: CurrentUser, todo: TodoUpdate):
    db_todo = session.scalar(select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id))

    if not db_todo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found')

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
