# SEO Admin Dashboard — Backend

Centralized Wagtail CMS backend that manages content for multiple websites. Frontend sites live on separate servers and consume content via the Wagtail REST API.

## What's in this repo

```
SEO-Dashboard/
├── admindashboard/          # Django / Wagtail CMS backend
├── docker-compose.prod.yml  # Production: backend + PostgreSQL
├── .env.example             # Environment variables template
├── README.md
└── OVERVIEW.md
```

## Deploy to production

**1. Create your `.env` from the template:**

```bash
cp .env.example .env
```

Edit `.env` — at minimum set `DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD`.

**2. Build and start:**

```bash
docker compose -f docker-compose.prod.yml --env-file .env up -d --build
```

**3. Create a superuser (first time only):**

```bash
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

**4. Stop:**

```bash
docker compose -f docker-compose.prod.yml down
```

## Services

| Service | URL | Description |
|---|---|---|
| Wagtail Admin | `http://<host>:8000/admin` | Content management |
| Wagtail API | `http://<host>:8000/api/v2/` | REST API for frontends |

## Architecture decisions

- **PostgreSQL** — replaces SQLite for production reliability
- **`depends_on: service_healthy`** — backend waits for Postgres to pass its health check before running migrations
- **WhiteNoise** — serves static files directly from Gunicorn, no Nginx needed
- **Named Docker volumes** — `postgres_data` and `media_data` survive container rebuilds
- **Multi-site** — one backend manages any number of frontend websites deployed on separate servers
