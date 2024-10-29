FROM python:3.11-alpine3.20

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0

RUN mkdir /app /app/staticfiles /app/media

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install poetry==1.8.3

COPY pyproject.toml poetry.lock ./

RUN poetry show \
    && apk update \
    && apk add --no-cache gcc pkgconf libpq-dev gettext build-base \
    && poetry update \
    && poetry install --no-root --no-dev \
    && poetry show --tree

COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8030
