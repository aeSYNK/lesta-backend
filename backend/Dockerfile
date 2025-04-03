FROM python:3.13-slim

ARG DJANGO_ENV
ENV DJANGO_ENV=${DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=2.1.2 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    build-essential \
    gcc \
    python3-dev &&\
    pip install --no-cache-dir \
    "poetry==$POETRY_VERSION" && \
    apt-get remove --purge -y build-essential python3-dev && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    poetry --version

WORKDIR /app

COPY ./backend /app/

# Project initialization:
RUN echo "$DJANGO_ENV" \
  && poetry install \
  $(if [ "$DJANGO_ENV" = 'production' ]; then echo '--no-test'; fi) \
  --no-interaction --no-ansi --no-root\
  # Cleaning poetry installation's cache for production:
  && if [ "$DJANGO_ENV" = 'Production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
