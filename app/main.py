from fastapi import FastAPI
from app.api import router as records_router

app = FastAPI(
    title="Records Collector API",
    description="A simple CRUD API for managing records",
    version="0.1.0",
)

app.include_router(records_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
