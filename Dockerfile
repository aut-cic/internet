FROM node:slim as frontend

WORKDIR /app

COPY frontend .

RUN npm install && npm run build

FROM python:3.11-rc-slim

RUN apt-get -y update \
  && apt-get --no-install-recommends -y install \
  build-essential \
  && rm -Rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=frontend /app/dist /app/frontend/dist
COPY . .
RUN pip install --upgrade pipenv
RUN pipenv install --system

# cleanup the apk cache
RUN rm -rf /var/cache/apk/*

EXPOSE 8080

# Entrypoint Script
ENTRYPOINT ["python3", "/app/main.py"]
