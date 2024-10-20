FROM python:3.12.6-slim
LABEL authors="jelmer"

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install && rm -rf $POETRY_CACHE_DIR

COPY graphpartition ./graphpartition
COPY website ./website
COPY manage.py ./manage.py

COPY start_django.sh ./
RUN chmod +x ./start_django.sh

ENTRYPOINT ["./start_django.sh"]