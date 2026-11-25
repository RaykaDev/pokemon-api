FROM python:3.13

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry

RUN poetry install --only main --no-root --no-interaction --no-ansi

COPY app/ ./app/

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
