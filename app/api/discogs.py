from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user
from app.services.discogs import discogs_service

router = APIRouter(prefix="/discogs", tags=["discogs"])

# In-memory storage for OAuth request tokens (in production, use Redis or similar)
oauth_requests: dict[str, tuple[str, str, int]] = {}


class DiscogsStatus(BaseModel):
    """Response model for Discogs connection status."""
    connected: bool
    discogs_username: str | None = None
    connected_at: str | None = None
    last_sync: str | None = None


class ImportResult(BaseModel):
    """Response model for collection import."""
    created: int
    updated: int
    errors: int
    message: str


@router.get("/status", response_model=DiscogsStatus)
def get_discogs_status(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get current Discogs connection status."""
    return DiscogsStatus(
        connected=current_user.discogs_access_token is not None,
        discogs_username=current_user.discogs_username,
        connected_at=current_user.discogs_connected_at.isoformat() if current_user.discogs_connected_at else None,
        last_sync=current_user.last_discogs_sync.isoformat() if current_user.last_discogs_sync else None,
    )


@router.get("/connect")
def connect_discogs(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Start Discogs OAuth flow.
    Returns URL to redirect user to for Discogs authorization.
    """
    authorize_url, request_token, request_token_secret = discogs_service.get_authorize_url()

    # Store request tokens temporarily (keyed by request_token)
    oauth_requests[request_token] = (request_token, request_token_secret, current_user.id)

    return {"authorize_url": authorize_url}


@router.get("/callback")
def discogs_callback(
    oauth_token: str,
    oauth_verifier: str,
    db: Annotated[Session, Depends(get_db)],
):
    """
    OAuth callback endpoint.
    Discogs redirects here after user authorizes the app.
    """
    # Retrieve stored request tokens
    if oauth_token not in oauth_requests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OAuth request",
        )

    request_token, request_token_secret, user_id = oauth_requests.pop(oauth_token)

    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    try:
        # Complete OAuth flow
        access_token, access_token_secret, discogs_username = discogs_service.complete_oauth(
            request_token, request_token_secret, oauth_verifier
        )

        # Save tokens to user
        discogs_service.save_user_tokens(
            db, user, access_token, access_token_secret, discogs_username
        )

        return {
            "message": "Successfully connected to Discogs",
            "discogs_username": discogs_username,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to complete OAuth: {str(e)}",
        )


@router.post("/import", response_model=ImportResult)
def import_collection(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Import collection from Discogs.
    Updates existing records or creates new ones.
    """
    if not current_user.discogs_access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discogs account not connected. Use /discogs/connect first.",
        )

    try:
        stats = discogs_service.import_collection(db, current_user)
        return ImportResult(
            created=stats["created"],
            updated=stats["updated"],
            errors=stats["errors"],
            message=f"Import complete: {stats['created']} created, {stats['updated']} updated, {stats['errors']} errors",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}",
        )


@router.post("/disconnect")
def disconnect_discogs(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Disconnect Discogs account."""
    if not current_user.discogs_access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discogs account not connected",
        )

    discogs_service.disconnect(db, current_user)
    return {"message": "Discogs account disconnected"}
