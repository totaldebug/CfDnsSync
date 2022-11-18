# ---- Base ----
FROM python:3.11-alpine3.16 AS base

WORKDIR /app

#
# ---- Dependencies ----
FROM base as build

RUN apt-get update \
    && apt-get install curl -y \
    && curl -sSL https://install.python-poetry.org | python

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

FROM dependencies AS release
COPY cfdnssync ./cfdnssync

ENV \
    CDS_CONFIG_DIR=/app/config \
    CDS_LOG_DIR=/app/config \
    PUID=1001 \
    PGID=1001 \
    PYTHONUNBUFFERED=1 \
    CRON='0 */12 * * *'

VOLUME /app/config

CMD ["python", "-m", "plextraktsync"]
