# CLAUDE.md

Guidance for working in this repository.

## What this is

The **AUT Internet System** — a FastAPI service that serves the login page for
Amirkabir University's internet, forwards credentials to the MikroTik server, and
reports usage from the FreeRADIUS database. See `README.md` for the architecture
diagram and local-dev instructions.

- Backend: Python (>= 3.14), FastAPI + SQLAlchemy + uvicorn, managed with `uv`.
- Frontend: TypeScript + webpack + Bootstrap, built into `frontend/dist`.
- Config: `dynaconf`, prefixed `INTERNET_` env vars (see `internet/conf/config.py`).

## Common commands (see `justfile`)

```bash
just install   # npm install + uv sync --all-groups
just build     # build the frontend bundle
just lint      # ruff + ty + djlint + biome + tsc
just test      # pytest
just update    # npm update + uv lock --upgrade
just run       # build frontend and run the server locally
```

CI (`.github/workflows/ci.yml`) runs ruff (check + format), `ty`, pytest and
djlint for Python, and biome + `tsc --noEmit` + the webpack build for the
frontend, on every push. It builds/pushes the Docker image on tag pushes.

## Structural things worth knowing

- **Route order is load-bearing.** `site_router` owns a `/{path:path}` catch-all
  that answers *every* path with the login page (MikroTik forwards arbitrary
  URLs to us, and iOS needs a 200). Any new router must be included *before* it
  in `create_app`, or it will silently never be reached. `/health` and
  `/metrics` used to be registered after it and were shadowed for exactly this
  reason — `tests/test_http.py` guards against a regression.
- **`internet.metrics` must be imported before `prometheus_client`.** The
  library picks in-process vs. multiprocess value classes at import time, based
  on `PROMETHEUS_MULTIPROC_DIR`. That module sets the variable and is the only
  place allowed to import `prometheus_client`; everything else goes through
  `render_latest()`. The Dockerfile also sets the variable as an `ENV`.
- **No module-level app state.** The engine and URLs live on `app.state` and are
  read via `request.app.state` in `internet/http/dependencies.py`, so
  `create_app` is a real factory and tests can build independent apps.
- **Model nullability mirrors `migrations/*.sql`.** In particular a NULL
  `acctstoptime` is what marks a session as still active.

## Release process

Releases follow SemVer (`vMAJOR.MINOR.PATCH`). Package-only updates are a patch;
notable-but-compatible build/runtime changes are a minor.

The production host (`internet-prod.aut.infra`) is **air-gapped — it has no
internet access**, so the image is built in CI, pulled/saved on a machine that
*does* have internet, copied over with `scp`, and `docker load`ed on the box.
The deploy tooling lives in the sibling repo `../ansible`.

### 1. Pre-flight

- Make sure `main` is green in CI and the working tree is clean.
- Decide the next version (`git tag --sort=-creatordate | head`).

### 2. Tag and let CI build the image

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z ..."
git push origin vX.Y.Z
```

On a `v*` tag push, CI builds and pushes `ghcr.io/aut-cic/internet:vX.Y.Z`
(`linux/amd64`, defined in `docker-bake.json`) to GHCR. Wait for it to go green:

```bash
gh run watch "$(gh run list --workflow ci.yml --branch vX.Y.Z --limit 1 --json databaseId --jq '.[0].databaseId')" --exit-status
```

Gotchas:
- The repo is sometimes **archived** (read-only). Unarchive before pushing:
  `gh repo unarchive aut-cic/internet --yes`.
- Pushes go over **SSH** (`git@github.com`). The `gh` OAuth token may lack the
  `workflow` scope, so it cannot merge/modify `.github/workflows/*` via the API —
  edit and push workflow changes with git over SSH instead.

### 3. Pull, save, and copy the image to production

Use `../ansible/update-internet-image.sh` (bump its `version=` first), or run the
steps directly:

```bash
docker pull ghcr.io/aut-cic/internet:vX.Y.Z --platform linux/amd64
docker save -o internet-vX.Y.Z.tar.gz ghcr.io/aut-cic/internet:vX.Y.Z
scp -C internet-vX.Y.Z.tar.gz internet-prod.aut.infra:/home/parham/
```

A local Docker daemon is required (e.g. `colima start`).

### 4. Load and restart on the production host

```bash
ssh internet-prod.aut.infra
docker load -i ~/internet-vX.Y.Z.tar.gz
# bump the running tag (compose lives at ~/aut-cic/docker-compose.yml)
sed -i -E 's#(ghcr\.io/aut-cic/internet:)[^"]+#\1vX.Y.Z#' ~/aut-cic/docker-compose.yml
docker compose -f ~/aut-cic/docker-compose.yml up -d
```

Also bump the image tag in `../ansible/internet/docker-compose.yml` and commit it
so the tracked deploy config stays in sync.

### 5. Verify

```bash
docker inspect --format '{{.State.Health.Status}}' aut-cic-internet-1   # -> healthy
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/         # -> 200

# /health must be JSON, not the login page
curl -s http://localhost:8080/health                                    # -> {"status":"healthy"}

# /metrics must contain the app's own counters, not just process defaults
curl -s http://localhost:8080/metrics | grep requests_total
```

Check `/health` and `/metrics` by **content**, not just status code. Both sit
behind the `/{path:path}` catch-all, so a shadowed route still answers 200 with
the login page — which is how they went unnoticed as broken. `grep
requests_total` is what actually proves multiprocess metrics are wired up.

App logs are not readable via `docker logs` because the production compose sets
`logging: driver: none`.

### 6. Create the GitHub release

```bash
gh release create vX.Y.Z --title vX.Y.Z --generate-notes
```

## Docker notes

- `Dockerfile` is multi-stage: a `node` stage builds the frontend, a
  `python:3.14-alpine` stage installs deps with `uv` and runs the app as a
  **non-root** user (`app`, uid 100) from the project venv.
- Base images and the `uv` binary are pinned; bump them deliberately.
- `docker-compose.yml` is for **local dev only** (spins up a MySQL with the
  `migrations/` seed data); production uses the compose file on the host.
