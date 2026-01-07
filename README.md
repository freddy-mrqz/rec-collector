# rec-collector

A FastAPI application for managing your vinyl record collection. Track your records, import from Discogs, and manage your collection with ease.

## Features

- **User Authentication** — Register and login with JWT-based authentication
- **Digital Collection Management** — Catalog your vinyl records with detailed metadata (artist, title, label, catalog number, condition, purchase info)
- **Discogs Integration** — Connect your Discogs account and import your entire collection with one click
- **Multi-user Support** — Each user has their own private collection
- **Play Tracking** — Log when you play records to see listening habits and identify neglected gems *(coming soon)*
- **Play Recommendations** — Get suggestions based on what you haven't played recently, mood, or genre *(coming soon)*

## Tech Stack

- **FastAPI** — Modern async Python web framework
- **Pydantic** — Data validation and serialization
- **SQLAlchemy** — ORM for database operations
- **python-jose** — JWT token handling
- **passlib** — Password hashing with bcrypt
- **python3-discogs-client** — Discogs API integration
- **Uvicorn** — ASGI server

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- Discogs developer account (for collection import feature)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/freddy-mrqz/rec-collector.git
   cd rec-collector
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set:
   - `SECRET_KEY` — Generate with `openssl rand -hex 32`
   - `TOKEN_ENCRYPTION_KEY` — Generate with `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
   - `DISCOGS_CONSUMER_KEY` and `DISCOGS_CONSUMER_SECRET` — Get from [Discogs Developer Settings](https://www.discogs.com/settings/developers)

### Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### API Documentation

Once running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Create a new account |
| POST | `/api/v1/auth/login` | Login and get JWT token |
| GET | `/api/v1/auth/me` | Get current user profile |

### Records (requires authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/records` | List your records |
| POST | `/api/v1/records` | Add a new record |
| GET | `/api/v1/records/{id}` | Get a specific record |
| PUT | `/api/v1/records/{id}` | Update a record |
| DELETE | `/api/v1/records/{id}` | Delete a record |

### Discogs Integration (requires authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/discogs/status` | Check Discogs connection status |
| GET | `/api/v1/discogs/connect` | Start OAuth flow (returns authorization URL) |
| GET | `/api/v1/discogs/callback` | OAuth callback (Discogs redirects here) |
| POST | `/api/v1/discogs/import` | Import collection from Discogs |
| POST | `/api/v1/discogs/disconnect` | Disconnect Discogs account |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

## Example Usage

### Register and Login

```bash
# Register a new user
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "vinyllover", "password": "securepass123"}'

# Login to get token
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -d "username=vinyllover&password=securepass123"
```

### Manage Records

```bash
# Set your token
TOKEN="your-jwt-token-here"

# Add a record
curl -X POST http://127.0.0.1:8000/api/v1/records \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Kind of Blue",
    "artist": "Miles Davis",
    "release_year": 1959,
    "label": "Columbia",
    "media_condition": "Very Good Plus"
  }'

# List your records
curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/v1/records
```

### Import from Discogs

```bash
# Start OAuth flow
curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/v1/discogs/connect
# Visit the returned authorize_url in your browser

# After authorizing, import your collection
curl -X POST -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/v1/discogs/import
```

## License

MIT
