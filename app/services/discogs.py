from datetime import datetime, timezone
from typing import Optional

import discogs_client
import traceback
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import encrypt_token, decrypt_token
from app.models.user import User
from app.models.record import Record

settings = get_settings()


class DiscogsService:
    """Service for Discogs OAuth and collection import."""

    def __init__(self):
        self.consumer_key = settings.discogs_consumer_key
        self.consumer_secret = settings.discogs_consumer_secret
        self.callback_url = settings.discogs_callback_url
        self.user_agent = "RecCollector/1.0"

    def get_oauth_client(self) -> discogs_client.Client:
        """Get a Discogs client for OAuth flow."""
        return discogs_client.Client(
            self.user_agent,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
        )

    def get_authorize_url(self) -> tuple[str, str, str]:
        """
        Start OAuth flow and return authorization URL.
        Returns: (authorize_url, request_token, request_token_secret)
        """
        client = self.get_oauth_client()
        request_token, request_token_secret, authorize_url = client.get_authorize_url(
            callback_url=self.callback_url
        )
        return authorize_url, request_token, request_token_secret

    def complete_oauth(
        self,
        request_token: str,
        request_token_secret: str,
        oauth_verifier: str,
    ) -> tuple[str, str, str]:
        """
        Complete OAuth flow with verifier from callback.
        Returns: (access_token, access_token_secret, discogs_username)
        """
        client = self.get_oauth_client()
        client.set_token(request_token, request_token_secret)
        access_token, access_token_secret = client.get_access_token(oauth_verifier)

        # Get the authenticated user's identity
        client.set_token(access_token, access_token_secret)
        identity = client.identity()

        return access_token, access_token_secret, identity.username

    def save_user_tokens(
        self,
        db: Session,
        user: User,
        access_token: str,
        access_token_secret: str,
        discogs_username: str,
    ) -> None:
        """Save encrypted Discogs tokens to user record."""
        user.discogs_access_token = encrypt_token(access_token)
        user.discogs_access_token_secret = encrypt_token(access_token_secret)
        user.discogs_username = discogs_username
        user.discogs_connected_at = datetime.now(timezone.utc)
        db.commit()

    def get_authenticated_client(self, user: User) -> Optional[discogs_client.Client]:
        """Get an authenticated Discogs client for a user."""
        if not user.discogs_access_token or not user.discogs_access_token_secret:
            return None

        access_token = decrypt_token(user.discogs_access_token)
        access_token_secret = decrypt_token(user.discogs_access_token_secret)

        client = discogs_client.Client(
            self.user_agent,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            token=access_token,
            secret=access_token_secret,
        )
        return client

    def import_collection(
        self,
        db: Session,
        user: User,
    ) -> dict:
        """
        Import user's Discogs collection.
        Updates existing records (matched by discogs_id) or creates new ones.
        Returns import statistics.
        """
        client = self.get_authenticated_client(user)
        if not client:
            raise ValueError("User not connected to Discogs")

        me = client.identity()
        collection = me.collection_folders[0]  # "All" folder

        stats = {"created": 0, "updated": 0, "errors": 0}

        for item in collection.releases:
            try:
                release = item.release
                discogs_id = str(release.id)

                # Check if record already exists for this user
                existing = (
                    db.query(Record)
                    .filter(
                        Record.user_id == user.id,
                        Record.discogs_id == discogs_id,
                    )
                    .first()
                )

                # Extract artist name(s)
                artists = ", ".join([a.name for a in release.artists]) if release.artists else "Unknown Artist"

                # Extract genres
                genres = ", ".join(g for g in release.genres) if release.genres else "N/A"

                # Extract label info
                label = None
                catalog_number = None
                if release.labels:
                    label = release.labels[0].name
                    catalog_number = release.labels[0].catno

                if existing:
                    # Update existing record with Discogs data
                    existing.title = release.title
                    existing.artist = artists
                    existing.genre = genres
                    existing.release_year = release.year if release.year else None
                    existing.label = label
                    existing.catalog_number = catalog_number
                    existing.imported_from_discogs = True
                    stats["updated"] += 1
                else:
                    # Create new record
                    new_record = Record(
                        user_id=user.id,
                        discogs_id=discogs_id,
                        title=release.title,
                        artist=artists,
                        genre=genres,
                        release_year=release.year if release.year else None,
                        label=label,
                        catalog_number=catalog_number,
                        imported_from_discogs=True,
                    )
                    db.add(new_record)
                    stats["created"] += 1

            except Exception:
                stats["errors"] += 1
                print('Error importing record: ')
                traceback.print_exc()
                continue

        # Update last sync time
        user.last_discogs_sync = datetime.now(timezone.utc)
        db.commit()

        return stats

    def disconnect(self, db: Session, user: User) -> None:
        """Remove Discogs connection from user."""
        user.discogs_access_token = None
        user.discogs_access_token_secret = None
        user.discogs_username = None
        user.discogs_connected_at = None
        db.commit()


# Singleton instance
discogs_service = DiscogsService()
