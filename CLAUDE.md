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
just install   # npm install + uv sync
just build     # build the frontend bundle
just lint      # ruff check/format + djlint
just update    # npm update + uv lock --upgrade
just run       # build frontend and run the server locally
uv run pytest  # run the Python tests
```

CI (`.github/workflows/ci.yml`) runs ruff, pytest, djlint, and the frontend build
on every push, and builds/pushes the Docker image on tag pushes.

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
curl -s http://localhost:8080/metrics | head                            # prometheus output
```

Note: the app takes ~15–20s to start (it pretty-prints all subnets and
announcements at import). App logs are not readable via `docker logs` because the
production compose sets `logging: driver: none`.

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
