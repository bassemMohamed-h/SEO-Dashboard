# PrimeShield Docker Setup

This repository includes a `docker-compose.yml` file to run both the frontend and backend together using Docker.

## Services

- `frontend`: Next.js application in `PrimeShield/`
- `backend`: Django/Wagtail application in `admindashboard/`

## Start with Docker

 run:

```bash
docker compose up --build
```

This will:
- build the frontend and backend images
- mount local source code into each container
- start the frontend on `http://localhost:3000`
- start the backend on `http://localhost:8000`

## Stop

Use:

```bash
docker compose down
```

## Notes

- The frontend container is configured to run `npm run dev`.
- The backend container uses the existing Python virtual environment setup from `admindashboard/Dockerfile`.
- If you change ports or service names, update `docker-compose.yml` accordingly.

## How to deploy:

# 1. Create your .env from the template
cp .env.example .env
# Edit .env — at minimum set DJANGO_SECRET_KEY and POSTGRES_PASSWORD

# 2. Build and start
docker compose -f docker-compose.prod.yml --env-file .env up -d --build

# 3. Create a superuser (first time only)
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
Key design decisions:

depends_on: condition: service_healthy — backend won't start until Postgres passes its health check, so migrations never race against a not-yet-ready DB
whitenoise serves static files directly from Gunicorn — no Nginx needed for this setup
Media uploads stored in a named Docker volume (media_data) so they survive container rebuilds
The dev docker-compose.yml is untouched — it still uses SQLite and dev settings