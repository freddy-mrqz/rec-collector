# rec-collector

A FastAPI application for managing your vinyl record collection. Track your records, log plays, and get recommendations for what to spin next or add to your collection.

## Features

- **Digital Collection Management** — Catalog your vinyl records with detailed metadata (artist, title, label, catalog number, condition, purchase info)
- **Play Tracking** — Log when you play records to see listening habits and identify neglected gems *(coming soon)*
- **Play Recommendations** — Get suggestions based on what you haven't played recently, mood, or genre *(coming soon)*
- **Purchase Recommendations** — Discover new records based on your collection and listening patterns *(coming soon)*
- **Discogs Integration** — Link records to Discogs for additional metadata *(coming soon)*

## Tech Stack

- **FastAPI** — Modern async Python web framework
- **Pydantic** — Data validation and serialization
- **SQLAlchemy** — ORM for database operations
- **Uvicorn** — ASGI server

## Getting Started

### Prerequisites

- Python 3.10+
- pip

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

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/records` | List all records |
| POST | `/api/v1/records` | Add a new record |
| GET | `/api/v1/records/{id}` | Get a specific record |
| PUT | `/api/v1/records/{id}` | Update a record |
| DELETE | `/api/v1/records/{id}` | Delete a record |
| GET | `/health` | Health check |

## Example Usage

**Add a record:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/records \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Kind of Blue",
    "artist": "Miles Davis",
    "release_year": 1959,
    "label": "Columbia",
    "media_condition": "Very Good Plus"
  }'
```

**List all records:**
```bash
curl http://127.0.0.1:8000/api/v1/records
```

## Project Structure

```
rec-collector/
├── app/
│   ├── api/
│   │   ├── __init__.py      # Router aggregation
│   │   └── records.py       # Record endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── record.py        # SQLAlchemy model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── record.py        # Pydantic schemas
│   ├── database.py          # Database configuration
│   └── main.py              # Application entry point
├── requirements.txt
└── README.md
```

## License

MIT
