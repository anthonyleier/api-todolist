from http import HTTPStatus

from fastapi import FastAPI

from app.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def index():
    return {'message': 'Hello World'}
