ARG NODE_VERSION=18
FROM node:${NODE_VERSION}-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y curl

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --uid ${UID} \
    appuser

COPY package*.json ./
RUN npm install --no-cache

COPY . .
RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 8080
