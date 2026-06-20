<h1 align="center">AUT Internet System</h1>

<p align="center">
  <img src="https://img.shields.io/github/actions/workflow/status/aut-cic/internet/ci.yml?label=ci&logo=github&style=for-the-badge&branch=main" alt="GitHub Workflow Status">
  <img alt="GitHub" src="https://img.shields.io/github/license/aut-cic/internet?logo=gnu&style=for-the-badge">
  <img alt="GitHub locked Python version" src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Faut-cic%2Finternet%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&style=for-the-badge&logo=python">
  <img alt="GitHub release (latest SemVer including pre-releases)" src="https://img.shields.io/github/v/release/aut-cic/internet?include_prereleases&logo=github&style=for-the-badge">
</p>

## Introduction

This service with the help of a MicroTik switch and Radius server meters students internet connections.
login page which is served by this server, fowards credentials to the MicroTik server and then uses
Radius information based on request's IP address to find out about internet usage status.

```mermaid
flowchart LR
    student["🧑‍🎓 Student device<br/>(browser)"]

    subgraph net["AUT network"]
        mikrotik["MikroTik switch/router<br/>(intercepts unauthenticated traffic)"]
        radius["FreeRADIUS server"]
        db[("FreeRADIUS DB<br/>radacct table")]
    end

    subgraph svc["This service (FastAPI)"]
        login["Login page<br/>GET /* → index.html"]
        status["Status page<br/>GET /status"]
        logout["Logout<br/>GET /logout/{sid}"]
        metrics["Metrics<br/>GET /metrics"]
    end

    %% Captive-portal redirect for users that are not logged in
    student -->|"1 - HTTP request"| mikrotik
    mikrotik -.->|"2 - redirect not-logged-in traffic"| login

    %% Authentication goes straight to MikroTik / RADIUS
    student -->|"3 - submit credentials"| mikrotik
    mikrotik -->|"4 - authenticate"| radius
    radius --> db

    %% This service identifies the user by client IP and reports usage
    login -->|"5 - IP → username"| db
    status -->|"usage by username"| db
    logout -->|"end session"| mikrotik

    %% Observability
    metrics -.->|Prometheus scrape| prom([Prometheus])
```

## How to run locally

For testing and development this server needs a free-radius database but here I created a `migrations` folder
that contains the database migrations and automatically runs by the `docker compose`. A user considers logged-in or out
based on his/her record in `radacct` table which is editable from the `migrations` folder. A record contains an IP
address and a logged-out date and when this logged-out time is `NULL` user consider as logged-in.

```bash
# database up and running based on /migrations
docker compose up -d

cd frontend && npm run build
uv sync

uv run python main.py

k6 run -u 1000 -i 1000 script.js
```

## Screenshots

![s1](./.github/assests/s1.png)

![s2](./.github/assests/s2.png)

![s3](./.github/assests/s3.png)
