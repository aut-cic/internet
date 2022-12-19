<h1 align="center">AUT Internet System</h1>

<p align="center">
  <img src="https://img.shields.io/github/actions/workflow/status/aut-cic/internet/ci.yml?label=ci&logo=github&style=for-the-badge&branch=main" alt="GitHub Workflow Status">
  <img alt="GitHub" src="https://img.shields.io/github/license/aut-cic/internet?logo=gnu&style=for-the-badge">
  <img alt="GitHub Pipenv locked Python version" src="https://img.shields.io/github/pipenv/locked/python-version/aut-cic/internet?logo=python&style=for-the-badge">
  <img alt="GitHub release (latest SemVer including pre-releases)" src="https://img.shields.io/github/v/release/aut-cic/internet?include_prereleases&logo=github&style=for-the-badge">
</p>

## Introduction

This service with the help of a MicroTik switch and Radius server meters students internet connections.
login page which is served by this server, fowards credentials to the MicroTik server and then uses
Radius information based on request's IP address to find out about internet usage status.

## How to run locally

For testing and development this server needs a free-radius database but here I created a `migrations` folder
that contains the database migrations and automatically runs by the `docker-compose`. A user considers logged-in or out
base on his/her record in `radacct` table which is editable from the `migrations` folder. A record contains an IP
address and a logged-out date and when this logged-out time is `NULL` user consider as logged-in.

```bash
# database up and running based on /migrations
docker-compose up -d

# frontend javascript and css
cd frontend && npm run build
pipenv install

# python pipenv shell
pipenv shell
python main.py

# k6 load testing
k6 run -u 1000 -i 1000 script.js
```

## Screenshots

![s1](./.github/assests/s1.png)

![s2](./.github/assests/s2.png)

![s3](./.github/assests/s3.png)
