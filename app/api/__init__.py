from fastapi import APIRouter
from app.api.records import router as records_router
from app.api.auth import router as auth_router

router = APIRouter()
router.include_router(records_router)
router.include_router(auth_router)

__all__ = ["router"]
