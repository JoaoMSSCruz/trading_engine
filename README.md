If still haven't a docker build run or changed requirements.txt or Dockerfile, run:
docker compose up -d --build

Else run:
docker compose restart trading-engine

In order to see the logs, run:
docker compose logs -f trading-engine