from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Todo, User
from app.schemas import TodoPublic, TodoSchema
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
