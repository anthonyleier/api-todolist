FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=FALSE

WORKDIR /app/
COPY . .

RUN pip install --no-cache-dir poetry==1.8.4
RUN poetry config installer.max-workers 10 && poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "app.main:app"]
