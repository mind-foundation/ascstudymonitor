# Build JS app
FROM node:12.18-alpine AS builder

RUN apk --no-cache add yarn
RUN mkdir -p /app/client
WORKDIR /client

COPY client/package.json ./
COPY client/yarn.lock ./
RUN yarn install

ADD ./client /client
ARG SOURCE_COMMIT
RUN yarn build

# Backend Target
FROM python:3.7-slim AS backend
RUN apt-get update && apt-get install -y git-core

EXPOSE 8000
WORKDIR /app/backend

RUN pip install poetry
COPY ./backend/pyproject.toml ./backend/poetry.lock /app/backend/
RUN poetry install --no-dev

ADD . /app
COPY --from=builder /client/dist/*.html /app/client/dist/

CMD ["poetry", "run", "gunicorn", "-c", "/app/etc/gunicorn.py", "ascmonitor.app:app"]
