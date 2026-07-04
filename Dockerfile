FROM python:3.12-slim

LABEL maintainer="João Cruz"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    make \
    dumb-init \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m quantuser

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY --chown=quantuser:quantuser . .

RUN pip install --no-cache-dir .

USER quantuser

EXPOSE 9000

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["python", "-m", "trading_engine"]