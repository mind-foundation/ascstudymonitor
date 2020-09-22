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

# Dev nginx target
FROM nginx:latest AS nginx-dev
COPY /backend/sitemap/robots.txt /srv
COPY --from=builder /client/dist/css /srv/css
COPY --from=builder /client/dist/js /srv/js
COPY --from=builder /client/dist/img /srv/img
