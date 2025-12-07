FROM node:slim AS frontend

WORKDIR /app

COPY frontend .

RUN npm install && npm run build

FROM python:3.14-alpine

# Install build dependencies
RUN apk --no-cache add build-base

# Copy uv binary from official image (pinned version for reproducibility)
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (without the project itself for caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Copy frontend build output
COPY --from=frontend /app/dist /app/frontend/dist

# Copy the rest of the application
COPY . .

# Install the project (compile bytecode for faster startup)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --compile-bytecode

EXPOSE 8080

ENTRYPOINT ["uv", "run", "python3", "/app/main.py"]
