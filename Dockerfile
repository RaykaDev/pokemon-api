FROM python:3.13

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry

ENV POETRY_VIRTUALENVS_CREATE=false

RUN poetry install --only main --no-root

COPY app/ ./app/

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]