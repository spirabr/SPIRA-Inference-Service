# --- base image --- #
FROM python:3.8 as mlflow_base

ENV POETRY_VERSION=1.3.2 

WORKDIR /project

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock .tool-versions ./

RUN poetry install --no-interaction --no-ansi --no-root

EXPOSE 5000

# --- base image --- #

