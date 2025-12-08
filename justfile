default:
    just --list

# build frontend package
build: install
    cd frontend && npm run build

# install python and nodejs packages
install:
    cd frontend && npm install
    uv sync

# update python and nodejs packages
update:
    cd frontend && npm update
    uv lock --upgrade

lint:
    uv run ruff check
    uv run ruff format
    uv run djlint --profile jinja templates -i 'H021,H031,H006,J018'

# build frontend and run the server
run: build
    uv run python main.py

# build and run the app in a container with database
run-container:
    docker compose --profile app up --build

# set up the dev environment with docker-compose
dev cmd *flags:
    #!/usr/bin/env bash
    set -euxo pipefail
    if [ {{ cmd }} = 'down' ]; then
      docker compose ./docker-compose.yml down --volumes
      docker compose ./docker-compose.yml rm
    elif [ {{ cmd }} = 'up' ]; then
      docker compose up -d {{ flags }}
    else
      docker compose {{ cmd }} {{ flags }}
    fi

# connect into the dev environment database
database: (dev "up") (dev "exec" "radius-db mysql --host=127.0.0.1 --user=opnsense --password=opnsense@123 --database=radius")
