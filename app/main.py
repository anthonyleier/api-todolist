from http import HTTPStatus

from fastapi import FastAPI

from app.routers import auth, todos, users
from app.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def index():
    return {'message': 'Hello World'}
