
# --- base image --- #
FROM python:3.8 as base

ENV POETRY_VERSION=1.3.2

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

WORKDIR /app

EXPOSE 8000

# --- base image --- #

# --- image with tests --- #
FROM base as dev

COPY pyproject.toml poetry.lock /app/ 

RUN poetry install --no-interaction --no-ansi

COPY . .

# --- image with tests --- #

# --- production image --- #
FROM base as prod

COPY pyproject.toml poetry.lock init.py /app/

RUN poetry install --no-interaction --no-ansi --no-dev

COPY --from=dev /app/src /app 

CMD ["main.py"]

# --- production image --- #

