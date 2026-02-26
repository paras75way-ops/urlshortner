from sqlmodel import Session
from fastapi import HTTPException
from datetime import datetime, timezone
from typing import Optional

from app.models.url import Url
from app.schema.url_schema import ShortenUrlRequest, ShortenUrlResponse, UrlDetailResponse
from app.repostries.url_repository import UrlRepository
from app.core.short_code import generate_short_code
from app.config import BASE_URL


class UrlService:

    def __init__(self, session: Session):
        self.repo = UrlRepository(session)

    def create_short_url(self, request: ShortenUrlRequest) -> ShortenUrlResponse:
        # Validate expiration is in the future
        if request.expires_at:
            now = datetime.now(timezone.utc)
            exp = request.expires_at
            # Handle naive datetime (treat as UTC)
            if exp.tzinfo is None:
                now = now.replace(tzinfo=None)
            if exp <= now:
                raise HTTPException(
                    status_code=422,
                    detail="Expiration time must be greater than the current time."
                )

        # If custom alias provided, check uniqueness
        if request.custom_alias:
            existing = self.repo.get_by_custom_alias(request.custom_alias)
            if existing:
                raise HTTPException(
                    status_code=409,
                    detail=f"Custom alias '{request.custom_alias}' is already taken."
                )
            short_code = request.custom_alias
            # Also check short_code collision
            if self.repo.get_by_short_code(short_code):
                raise HTTPException(
                    status_code=409,
                    detail=f"Short code '{short_code}' is already in use."
                )
        else:
            # Generate unique short code with collision check
            short_code = generate_short_code()
            retries = 0
            while self.repo.get_by_short_code(short_code) and retries < 5:
                short_code = generate_short_code()
                retries += 1

        url = Url(
            short_code=short_code,
            original_url=str(request.original_url),
            custom_alias=request.custom_alias,
            title=request.title,
            expires_at=request.expires_at,
        )

        created = self.repo.create(url)

        return ShortenUrlResponse(
            id=created.id,
            short_code=created.short_code,
            short_url=f"{BASE_URL}/{created.short_code}",
            original_url=created.original_url,
            title=created.title,
            created_at=created.created_at,
        )

    def resolve_url(self, short_code: str) -> Url:
        url = self.repo.get_by_short_code(short_code)
        if not url:
            raise HTTPException(status_code=404, detail="Short URL not found.")

        if not url.is_active:
            raise HTTPException(status_code=410, detail="This short URL has been deactivated.")

        if url.expires_at:
            now = datetime.now(timezone.utc)
            exp = url.expires_at
            if exp.tzinfo is None:
                now = now.replace(tzinfo=None)
            if exp < now:
                raise HTTPException(status_code=410, detail="This short URL has expired.")

        return url

    def get_url_details(self, short_code: str) -> UrlDetailResponse:
        url = self.repo.get_by_short_code(short_code)
        if not url:
            raise HTTPException(status_code=404, detail="Short URL not found.")

        return UrlDetailResponse(
            id=url.id,
            short_code=url.short_code,
            short_url=f"{BASE_URL}/{url.short_code}",
            original_url=url.original_url,
            title=url.title,
            custom_alias=url.custom_alias,
            is_active=url.is_active,
            click_count=url.click_count,
            created_at=url.created_at,
            expires_at=url.expires_at,
        )

    def list_urls(self, skip: int = 0, limit: int = 50) -> tuple[list[UrlDetailResponse], int]:
        urls = self.repo.get_all(skip=skip, limit=limit)
        total = self.repo.count_all()

        details = [
            UrlDetailResponse(
                id=u.id,
                short_code=u.short_code,
                short_url=f"{BASE_URL}/{u.short_code}",
                original_url=u.original_url,
                title=u.title,
                custom_alias=u.custom_alias,
                is_active=u.is_active,
                click_count=u.click_count,
                created_at=u.created_at,
                expires_at=u.expires_at,
            )
            for u in urls
        ]
        return details, total

    def deactivate_url(self, short_code: str) -> None:
        url = self.repo.deactivate(short_code)
        if not url:
            raise HTTPException(status_code=404, detail="Short URL not found.")
