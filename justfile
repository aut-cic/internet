default:
    just --list

# build frontend package
build: install
    cd frontend && npm run build

# install python and nodejs packages
install:
    cd frontend && npm install
    pipenv install --dev -v

# update python and nodejs packages
update:
    cd frontend && npm update
    pipenv update

lint:
    pipenv run mypy .
    pipenv run djlint --profile jinja templates -i 'H021,H031,H006,J018'
    pipenv run pylint --enable-all-extensions --fail-under 8 internet

# set up the dev environment with docker-compose
dev cmd *flags:
    #!/usr/bin/env bash
    set -euxo pipefail
    if [ {{ cmd }} = 'down' ]; then
      docker compose -f ./docker-compose.yml down
      docker compose -f ./deployments/docker-compose.yml rm
    elif [ {{ cmd }} = 'up' ]; then
      docker compose -f ./docker-compose.yml up -d {{ flags }}
    else
      docker compose -f ./docker-compose.yml {{ cmd }} {{ flags }}
    fi

# connect into the dev environment database
database: (dev "up") (dev "exec" "radius-db mysql --host=127.0.0.1 --user=opnsense --password=opnsense@123 --database=radius")
