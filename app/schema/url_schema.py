from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional
import uuid


class ShortenUrlRequest(BaseModel):
    original_url: HttpUrl
    custom_alias: Optional[str] = None
    title: Optional[str] = None
    expires_at: Optional[datetime] = None


class ShortenUrlResponse(BaseModel):
    id: uuid.UUID
    short_code: str
    short_url: str
    original_url: str
    title: Optional[str] = None
    created_at: datetime


class UrlDetailResponse(BaseModel):
    id: uuid.UUID
    short_code: str
    short_url: str
    original_url: str
    title: Optional[str] = None
    custom_alias: Optional[str] = None
    is_active: bool
    click_count: int
    created_at: datetime
    expires_at: Optional[datetime] = None


class UrlListResponse(BaseModel):
    urls: list[UrlDetailResponse]
    total: int


class MessageResponse(BaseModel):
    message: str
