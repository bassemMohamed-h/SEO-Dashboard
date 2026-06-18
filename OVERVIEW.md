# SEO Dashboard — Project Overview

A centralized CMS & SEO admin dashboard for managing multiple websites from a single control panel. Built on a headless architecture: **Wagtail CMS** powers the backend content management, and **Next.js** drives each managed website as a fast, SEO-optimized frontend.

---

## Purpose

Instead of logging into a separate admin panel for every website, editors and SEO managers use one dashboard (Wagtail admin) to create, update, and publish content across any number of sites. Each website consumes content via a REST API, so the frontend is fully decoupled and can be deployed independently.

---

## Architecture

```
┌─────────────────────────────────┐       ┌───────────────────────────┐
│   Wagtail Admin (Django)        │  API  │   Next.js Frontend        │
│   /admin  —  port 8000          │──────▶│   primeshield.com         │
│                                 │       │   port 3000               │
│  • Content editing              │       │                           │
│  • Page tree management         │       │  • SSR / SEO-optimized    │
│  • Image / document library     │       │  • Dynamic [slug] routing │
│  • Multi-site support           │       │  • Bilingual (AR / EN)    │
│  • REST API (Wagtail API v2)    │       │  • Sitemap auto-generated │
└─────────────────────────────────┘       └───────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| CMS / Admin | Wagtail 7.4 + Django 6 |
| API | Wagtail API v2 (pages, images, documents) |
| Frontend | Next.js 16 + React 19 |
| Styling | CSS Modules |
| Animations | AOS, Framer Motion, GSAP |
| Email | EmailJS |
| i18n | JSON message files (Arabic / English) |
| Database | SQLite (dev) |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
SEO-Dashboard/
├── docker-compose.yml              # Orchestrates frontend + backend
│
├── PrimeShield/                    # Next.js managed website
│   └── src/
│       ├── app/                    # Page routes
│       │   ├── page.js             # Home
│       │   ├── about/
│       │   ├── services/
│       │   ├── projects/
│       │   ├── certificates/
│       │   ├── contact/
│       │   ├── [slug]/             # Dynamic CMS-driven pages
│       │   └── sitemap.js          # Auto-generated sitemap
│       ├── components/
│       │   ├── common/             # Navbar, container, AOS provider
│       │   └── sections/           # Page sections (Hero, About, Services, …)
│       └── messages/
│           ├── ar.json             # Arabic translations
│           └── en.json             # English translations
│
└── admindashboard/            # Django / Wagtail CMS
    ├── backend/
    │   ├── settings/               # base / dev / production configs
    │   ├── api.py                  # Wagtail API router (pages, images, docs)
    │   └── urls.py
    ├── home/
    │   └── models.py               # Page models with StreamFields
    └── search/
        └── views.py
```

---

## Content Models

Content is built with Wagtail **StreamFields**, giving editors flexible, block-based page layouts.

| Model | Blocks |
|---|---|
| `HomePage` | Hero, About, Vision (slider), Services (grid) |
| `StandardPage` | RichText, Hero |

Each block exposes its data through the Wagtail API, which the Next.js frontend consumes at build time or request time.

---

## API Endpoints

Provided by Wagtail API v2 at `http://localhost:8000/api/v2/`:

| Endpoint | Description |
|---|---|
| `/api/v2/pages/` | All CMS pages with content |
| `/api/v2/images/` | Media library |
| `/api/v2/documents/` | Uploaded documents |

---

## Running the Project

**With Docker (recommended):**

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Wagtail Admin | http://localhost:8000/admin |
| Wagtail API | http://localhost:8000/api/v2/ |

**Without Docker:**

```bash
# Backend
cd admindashboard
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Frontend
cd PrimeShield
npm install
npm run dev
```

---

## Managed Websites

| Website | Frontend Directory | Notes |
|---|---|---|
| PrimeShield | `PrimeShield/` | Saudi waterproofing & insulation company — bilingual (AR/EN) |

> Additional websites are added as new Next.js apps pointing at the same Wagtail backend, taking advantage of Wagtail's built-in multi-site support.

---

## Key SEO Features

- **Server-side rendering** via Next.js for fast initial loads and crawler-friendly HTML
- **Auto-generated sitemap** (`/sitemap.js`) fed from CMS page tree
- **Dynamic `[slug]` routing** — new CMS pages are live immediately without frontend deploys
- **Bilingual support** (Arabic / English) with locale-aware content from the CMS
- **`robots.txt`** managed in the public directory
- **Clean URL structure** driven by Wagtail's page tree
