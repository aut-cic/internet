<h1 align="center">AUT Internet System</h1>

<p align="center">
  <img src="https://img.shields.io/github/workflow/status/aut-cic/internet/ci?label=ci&logo=github&style=for-the-badge" alt="GitHub Workflow Status">
  <img alt="GitHub" src="https://img.shields.io/github/license/aut-cic/internet?logo=gnu&style=for-the-badge">
  <img alt="GitHub Pipenv locked Python version" src="https://img.shields.io/github/pipenv/locked/python-version/aut-cic/internet?logo=python&style=for-the-badge">
  <img alt="GitHub release (latest SemVer including pre-releases)" src="https://img.shields.io/github/v/release/aut-cic/internet?include_prereleases&logo=github&style=for-the-badge">
</p>

## Introduction

This service with the help of a MicroTik switch and Radius server meters students internet connections.
login page which is served by this server fowards credentials to the microtik server and then uses
Radius information based on request ip address to find out about internet usage status.

## How to run locally

For testing and development this server needs a free-radius database but here I created a `migrations` folder
that contains the database migrations and automatically runs by the `docker-compose`. A user consider logged-in or out
base on his/her record in `radacct` table which is editable from the `migrations` folder. A record contains an IP
address and a logged-out date and when this logged-out time is `NULL` user consider as logged-in.

```sh
docker-compose up
cd frontend && npm run build
pipenv install
pipenv shell
python3 main.py
```

## Screenshots

![s1](./.github/assests/s1.png)

![s2](./.github/assests/s2.png)
