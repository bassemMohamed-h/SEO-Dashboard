# SEO Dashboard — Project Overview

A centralized CMS & SEO admin dashboard for managing multiple websites from a single control panel. Built on a headless architecture: **Wagtail CMS** powers the backend content management, and **Next.js** drives each managed website as a fast, SEO-optimized frontend deployed on its own server.

---

## Purpose

Instead of logging into a separate admin panel for every website, editors and SEO managers use one dashboard (Wagtail admin) to create, update, and publish content across any number of sites. Each website consumes content via a REST API, so the frontend is fully decoupled and deployed independently.

---

## Architecture

```
┌──────────────────────────────────────┐
│   SEO Admin Dashboard (this repo)    │
│   Django + Wagtail — port 8000       │
│   PostgreSQL database                │
│                                      │
│  • Content editing & publishing      │
│  • Image / document library          │
│  • Multi-site support                │
│  • REST API (Wagtail API v2)         │
└──────────┬───────────────────────────┘
           │  HTTP API  (per-site CORS)
     ┌─────┴──────────────────────────────────┐
     │                                        │
     ▼                                        ▼
┌─────────────────────┐          ┌─────────────────────┐
│  Next.js Site A     │          │  Next.js Site B      │
│  primeshield.com.sa │          │  civilia.com  (etc.) │
│  (separate server)  │          │  (separate server)   │
└─────────────────────┘          └─────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| CMS / Admin | Wagtail 7.4 + Django 6 |
| API | Wagtail API v2 — custom `MultiSitePagesAPIViewSet` |
| Database | PostgreSQL 16 (production) |
| Static files | WhiteNoise (served directly from Gunicorn) |
| App server | Gunicorn |
| Containerization | Docker + Docker Compose |

---

## Repository Structure

```
SEO-Dashboard/
├── docker-compose.prod.yml         # Production: backend + PostgreSQL
├── .env.example                    # All environment variable docs
│
└── admindashboard/                 # Django / Wagtail backend
    ├── Dockerfile                  # Multi-stage build (builder + runtime)
    ├── entrypoint.sh               # migrate → gunicorn on container start
    ├── requirements.txt
    ├── manage.py
    ├── backend/
    │   ├── settings/
    │   │   ├── base.py             # Shared settings
    │   │   ├── dev.py              # Local dev (SQLite)
    │   │   └── production.py       # Production (PostgreSQL, WhiteNoise, env vars)
    │   ├── api.py                  # MultiSitePagesAPIViewSet + router
    │   ├── urls.py
    │   └── wsgi.py
    ├── home/
    │   ├── models.py               # All page models (multi-site)
    │   └── migrations/
    ├── search/
    │   └── views.py
    └── media/                      # User-uploaded files (volume-mounted in prod)
```

---

## Page Models

| Model | Site | Description |
|---|---|---|
| `PrimeShieldHomePage` | primeshield.com.sa | Home page with hero, services, projects |
| `CiviliaNewsIndexPage` | civilia site | News listing index |
| `CiviliaNewsPage` | civilia site | Individual news article with cover image + rich text |
| `StandardPage` | any | Generic rich-text page |

New sites are added by creating a Wagtail `Site` record pointing to a root page, then building a Next.js frontend that fetches from `GET /api/v2/pages/?type=home.YourModel`.

---

## API

Base URL: `http://<host>:8000/api/v2/`

| Endpoint | Description |
|---|---|
| `GET /api/v2/pages/` | All published pages across all sites |
| `GET /api/v2/pages/?type=home.CiviliaNewsPage` | Filter by page type |
| `GET /api/v2/pages/?slug=blog-1` | Fetch by slug |
| `GET /api/v2/images/` | Media library |
| `GET /api/v2/documents/` | Uploaded documents |

The `MultiSitePagesAPIViewSet` skips Wagtail's default single-site filter, so all sites' pages are accessible from one endpoint. Pass `?site=hostname:port` to scope results to one site.

---

## Managed Websites

| Website | Domain | Stack | Server |
|---|---|---|---|
| PrimeShield | primeshield.com.sa | Next.js 16, bilingual AR/EN | separate |
| Civilia | — | Next.js + next-intl, bilingual AR/EN | separate |

> Adding a new website = new Wagtail `Site` + new page models + a new Next.js app deployed anywhere.

---

## Production Deployment

```bash
# 1. Configure secrets
cp .env.example .env   # then fill in DJANGO_SECRET_KEY, POSTGRES_PASSWORD, etc.

# 2. Build & start
docker compose -f docker-compose.prod.yml --env-file .env up -d --build

# 3. First-time superuser
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

Postgres data and uploaded media are stored in named Docker volumes and survive restarts and rebuilds.
