from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.api import router as api_router
from app.database import engine
from app.models import Base


def _run_migrations():
    """Add new columns to existing tables if they don't exist (SQLite compatible)."""
    new_columns = [
        ("records", "original_year", "INTEGER"),
        ("records", "image_url", "VARCHAR"),
    ]
    with engine.connect() as conn:
        for table, column, col_type in new_columns:
            existing = conn.execute(text(f"PRAGMA table_info({table})")).fetchall()
            if not any(row[1] == column for row in existing):
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
        conn.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)
    # Apply any new columns to existing tables
    _run_migrations()
    yield


app = FastAPI(
    title="Records Collector API",
    description="A simple CRUD API for managing records",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
