# syntax=docker/dockerfile:1

FROM node:24-slim AS frontend

WORKDIR /app

# Install dependencies first (reproducible) for better layer caching
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Build the frontend bundle
COPY frontend .
RUN npm run build

FROM python:3.14-alpine

# Build dependencies for any packages without musl wheels
RUN apk --no-cache add build-base

# Copy uv binary from the official image (pinned for reproducibility)
COPY --from=ghcr.io/astral-sh/uv:0.11.23 /uv /uvx /bin/

# uv runtime configuration
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH"

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
  uv sync --frozen --no-dev

# Run as an unprivileged user; ensure the metrics multiprocess dir is writable
RUN addgroup -S app && adduser -S -G app app \
  && mkdir -p /app/prom && chown -R app:app /app
USER app

EXPOSE 1378

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:1378/health || exit 1

ENTRYPOINT ["python", "/app/main.py"]
