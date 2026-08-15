# grumpygirl

**An anti-procrastination productivity app built around one question: _What should I do right now?_**

This repository contains a minimal runnable scaffold (Expo frontend + FastAPI backend + MongoDB) so you can run the MVP locally.

Quick start (recommended, from repo root):

1. Copy env files:

```bash
cp backend/.env.example backend/.env
```

2. Build and run with Docker Compose:

```bash
docker compose up --build
```

- API: http://localhost:8000
- Health: http://localhost:8000/health
- Expo frontend: run from `frontend/` (instructions below)

Backend can run without Docker as well — see backend/README.md.

If you change the repo name or host, update `EXPO_PUBLIC_BACKEND_URL` in `frontend/.env` or use the LAN IP for a physical phone.
