
# BUILD STAGE — installs system deps and compiles Python packages.
FROM python:3.12-slim-bookworm AS builder

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/* \
 && python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN pip install "gunicorn==25.1.0"


# RUNTIME STAGE
FROM python:3.12-slim-bookworm AS runtime

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libpq5 \
    libmariadb3 \
    libjpeg62-turbo \
    libwebp7 \
 && rm -rf /var/lib/apt/lists/*

RUN useradd wagtail

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
RUN chown wagtail:wagtail /app

COPY --chown=wagtail:wagtail . .

USER wagtail

# Collect static files using production settings.
# DJANGO_SECRET_KEY is a placeholder only for this build step — the real
# key is injected at runtime via the environment.
ARG DJANGO_SETTINGS_MODULE=backend.settings.production
ARG DJANGO_SECRET_KEY=collectstatic-build-placeholder
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} \
    DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

RUN python manage.py collectstatic --noinput --clear

ENTRYPOINT ["/app/entrypoint.sh"]
