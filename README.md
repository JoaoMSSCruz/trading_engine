If still haven't a docker build run or changed requirements.txt or Dockerfile, run:
docker compose up -d --build

Else run:
docker compose restart trading-engine

In order to see the logs, run:
docker compose logs -f trading-engine

Notes for the future:
-> I know that there are some design choices that cause an overhead, such as getters. The objective of this engine is not to operate at HFT latencies,
but to be scalable and relatively intuitive. The previous engines were functional but impossible to debug from an outsider's perspective,
that's why I created this one.

In order to connect to the broker, you must have a the .env file in the trading_engine directory. There is an example of how to do it in .env_example