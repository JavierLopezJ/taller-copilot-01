# JWT Backend API

FastAPI application that implements JWT (JSON Web Token) authentication.

## Features

- **POST /token** — Authenticate with username and password, receive an access token (300 s) and a refresh token (3600 s).
- **POST /token/refresh** — Exchange a valid refresh token for a new access token.
- **GET /health** — Health check endpoint.
- Interactive docs available at `/docs` (Swagger UI) and `/redoc`.

## Credentials

| Field    | Value      |
|----------|------------|
| username | `admin`    |
| password | `admin123` |

## Requirements

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Or [Python 3.11+](https://www.python.org/) and [Poetry](https://python-poetry.org/docs/#installation)

---

## Running with Docker Compose (recommended)

```bash
# From the backend/ directory
docker compose up --build
```

The API will be available at `http://localhost:8000`.

---

## Running locally with Poetry

```bash
# From the backend/ directory

# Install dependencies
poetry install

# Start the development server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Usage Examples

### 1. Obtain tokens

```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&******"
```

**Response:**
```json
{
  "access_token": "<jwt-access-token>",
  "refresh_token": "<jwt-refresh-token>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### 2. Refresh the access token

```bash
curl -X POST http://localhost:8000/token/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<jwt-refresh-token>"}'
```

**Response:**
```json
{
  "access_token": "<new-jwt-access-token>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### 3. Health check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{"status": "ok"}
```

---

## Interactive API Documentation

Once the server is running, open your browser at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI application and route definitions
│   ├── auth.py        # JWT creation, validation and user authentication logic
│   └── models.py      # Pydantic response models
├── pyproject.toml     # Poetry project and dependency configuration
├── Dockerfile         # Container image definition
├── docker-compose.yml # Multi-container orchestration
└── README.md          # This file
```

---

## Notes

- The `SECRET_KEY` in `app/auth.py` **must** be changed to a strong random value before deploying to production.  
  Generate one with: `openssl rand -hex 32`
- Access tokens expire after **300 seconds**; refresh tokens expire after **3600 seconds**.
