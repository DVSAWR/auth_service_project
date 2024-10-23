FROM python:3.12-slim

LABEL maintainer="gruzdev.daniil@gmail.com"

WORKDIR /workdir

ENV POETRY_VERSION=1.8.3

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="$PATH:/root/.local/bin"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY ./src/app ./app

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
