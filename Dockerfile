FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_CACHE_DIR=/.cache

COPY ./requirements.txt .

RUN --mount=type=cache,target=${PIP_CACHE_DIR},sharing=locked \
    pip install --ignore-installed -r ./requirements.txt

COPY . .
