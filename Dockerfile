# Build JS app
FROM node:12.18-alpine AS builder

RUN apk --no-cache add yarn
RUN mkdir -p /app/client
WORKDIR /client

COPY client/package.json ./
COPY client/yarn.lock ./
RUN yarn install

ADD ./client /client
ENV SOURCE_COMMIT $SOURCE_COMMIT
RUN yarn build

# Backend Target
FROM python:3.7-slim AS backend
RUN apt-get update && apt-get install -y git-core

EXPOSE 8000
WORKDIR /app

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry install

ADD . /app
COPY --from=builder /client/dist /app/client/dist

CMD ["poetry", "run", "gunicorn", "-w", "4", "--bind", "0.0.0.0:8000", "--timeout", "120", "--log-level", "info", "ascmonitor.app:app"]
