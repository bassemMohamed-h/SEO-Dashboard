# SEO Admin Dashboard

A single Wagtail CMS backend that manages content for any number of websites. Each website is a separate Next.js frontend deployed on its own server — the dashboard pushes content to all of them through a REST API.

---

## How it works

```
┌─────────────────────────────────────┐
│        SEO Admin Dashboard          │
│     Django + Wagtail — port 8000    │
│     PostgreSQL (prod) / SQLite (dev)│
│                                     │
│  • One admin panel for all sites    │
│  • 3 generic page types (no code    │
│    changes needed per new website)  │
│  • REST API consumed by frontends   │
└──────────┬──────────────────────────┘
           │  Wagtail API v2
     ┌─────┴──────────────────────────────────┐
     │                                        │
     ▼                                        ▼
┌─────────────────────┐          ┌──────────────────────┐
│  Next.js Site A     │          │  Next.js Site B       │
│  primeshield.com.sa │          │  civilia.com   (etc.) │
│  port 3000 (local)  │          │  port 3002 (local)    │
└─────────────────────┘          └──────────────────────┘
```

---

## Page structure (3 generic types — no backend changes per new site)

```
GenericHomePage          ← one per website
    └── GenericSectionPage   ← one per section (blogs, services, news, projects …)
            └── GenericDetailPage    ← one per item (post, service, article …)
```

| Type | Fields |
|---|---|
| `GenericHomePage` | `h1_title`, `meta_description`, `body` |
| `GenericSectionPage` | `h1_title`, `meta_description`, `body` |
| `GenericDetailPage` | `meta_description`, `date`, `excerpt`, `cover_image`, `body` |

`body` accepts Rich text, Images, and raw Embed HTML blocks — the frontend pulls and renders them.

Adding a new website = create a `GenericHomePage` in admin + register the site in **Settings → Sites**. No Python code needed.

---

## Repository structure

```
SEO-Dashboard/
├── docker-compose.dev.yml          # Dev: SQLite, hot reload, no secrets needed
├── docker-compose.prod.yml         # Prod: PostgreSQL, Gunicorn, WhiteNoise
├── .env                            # Production secrets (git-ignored)
├── .env.example                    # Docs for all env vars + dev instructions
│
└── admindashboard/
    ├── Dockerfile                  # Multi-stage production build
    ├── Dockerfile.dev              # Lightweight dev build (runserver)
    ├── entrypoint.sh               # migrate → gunicorn on prod container start
    ├── requirements.txt
    ├── backend/
    │   ├── settings/
    │   │   ├── base.py             # Shared settings, CORS for localhost:3000 & 3002
    │   │   ├── dev.py              # SQLite, DEBUG=True, ALLOWED_HOSTS=*
    │   │   └── production.py       # PostgreSQL, WhiteNoise, all config from env vars
    │   ├── api.py                  # MultiSitePagesAPIViewSet (serves all sites from one endpoint)
    │   └── urls.py
    └── home/
        ├── models.py               # GenericHomePage, GenericSectionPage, GenericDetailPage
        └── migrations/
```

---

## Dev mode (local testing)

No `.env` or database setup needed — uses SQLite automatically.

```bash
# Start the backend
docker compose -f docker-compose.dev.yml up --build

# First time — create an admin user
docker compose -f docker-compose.dev.yml exec backend python manage.py createsuperuser
```

Admin: `http://localhost:8000/admin/`
API: `http://localhost:8000/api/v2/`

**Connect local frontends** — add to each frontend project's `.env.local`:
```env
NEXT_PUBLIC_WAGTAIL_API_URL=http://localhost:8000/api/v2
```

CORS for `localhost:3000` and `localhost:3002` is pre-configured in `base.py`.

---

## Production deployment (VPS)

```bash
# 1. Set secrets
cp .env.example .env
# Edit .env — set DJANGO_SECRET_KEY, POSTGRES_PASSWORD, DJANGO_ALLOWED_HOSTS, etc.

# 2. Build and start
docker compose -f docker-compose.prod.yml --env-file .env up -d --build

# 3. First-time superuser
docker compose -f docker-compose.prod.yml exec \
  -e DJANGO_SUPERUSER_USERNAME=admin \
  -e DJANGO_SUPERUSER_EMAIL=admin@example.com \
  -e DJANGO_SUPERUSER_PASSWORD=YourPassword \
  backend python manage.py createsuperuser --noinput

# 4. Stop
docker compose -f docker-compose.prod.yml down
```

**Services:**

| Service | URL |
|---|---|
| Wagtail Admin | `https://seodashboard.respect-solutions.cloud/admin/` |
| Wagtail API | `https://seodashboard.respect-solutions.cloud/api/v2/` |

---

## API quick reference

```
# Home page of a site
GET /api/v2/pages/?type=home.GenericHomePage&slug=primeshield&fields=h1_title,meta_description,body

# Section listing (e.g. blogs)
GET /api/v2/pages/?type=home.GenericSectionPage&slug=blogs&fields=h1_title,meta_description,body

# All items in a section
GET /api/v2/pages/?type=home.GenericDetailPage&child_of=<section_id>&fields=date,excerpt,cover_image&order=-date

# Single detail page
GET /api/v2/pages/?type=home.GenericDetailPage&slug=my-post&fields=meta_description,date,excerpt,cover_image,body

# Images
GET /api/v2/images/
```

---

## Managed websites

| Website | Domain | Stack |
|---|---|---|
| PrimeShield | primeshield.com.sa | Next.js 16, bilingual AR/EN |
| Civilia | civiliadevelopments.respect-solutions.com | Next.js + next-intl, bilingual AR/EN |

> To add a new website: create a `GenericHomePage` in admin, add it under **Settings → Sites**, build a Next.js frontend that fetches from the API. No backend code changes required.

---

## Key decisions

- **3 generic page types** — `GenericHomePage`, `GenericSectionPage`, `GenericDetailPage` cover every content pattern. No site-specific models.
- **`MultiSitePagesAPIViewSet`** — overrides Wagtail's default single-site filter so all sites share one API endpoint.
- **WhiteNoise** — static files served directly from Gunicorn in production, no Nginx needed.
- **Named Docker volumes** — `postgres_data` and `media_data` survive rebuilds.
- **`depends_on: service_healthy`** — backend waits for Postgres health check before running migrations.
