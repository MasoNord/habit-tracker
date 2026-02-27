FROM python:3.12-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

RUN pip install poetry

COPY pyproject.toml poetry.lock README.md ./
COPY src ./src

RUN poetry lock \
    && poetry install --only main

RUN chmod +x ./entrypoint.sh


FROM python-base as production

WORKDIR /app

ENV PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    file \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder-base /opt /opt

COPY . .

EXPOSE 8000

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]