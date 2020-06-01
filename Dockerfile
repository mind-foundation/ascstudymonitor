# Build JS app
FROM node:current-alpine AS builder

RUN apk --no-cache add yarn
RUN mkdir -p /app/client
WORKDIR /app/client

COPY client/package*.json ./
COPY client/yarn.lock ./
RUN yarn install

ADD . /app
ENV SOURCE_COMMIT $SOURCE_COMMIT
RUN yarn build

# Install python requirements
FROM python:3.7-slim
RUN apt-get update && apt-get install -y git-core

EXPOSE 8000
WORKDIR /app

RUN pip install poetry
copy ./pyproject.toml ./poetry.lock /app/
RUN poetry install

ADD . /app
COPY --from=builder /app/client /app/client

CMD ["poetry", "run", "gunicorn", "-w", "4", "--bind", "0.0.0.0:8000", "--timeout", "120", "ascmonitor.app:app"]
