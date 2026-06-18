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
