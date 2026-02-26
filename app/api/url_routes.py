from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.db.db import get_session
from app.schema.url_schema import (
    ShortenUrlRequest,
    ShortenUrlResponse,
    UrlDetailResponse,
    UrlListResponse,
    MessageResponse,
)
from app.schema.analytics_schema import AnalyticsSummary
from app.services.url_service import UrlService
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/urls", tags=["URLs"])


@router.post("/shorten", response_model=ShortenUrlResponse, status_code=201)
def shorten_url(
    request: ShortenUrlRequest,
    session: Session = Depends(get_session),
):
     
    service = UrlService(session)
    return service.create_short_url(request)


@router.get("", response_model=UrlListResponse)
def list_urls(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: Session = Depends(get_session),
):
     
    service = UrlService(session)
    urls, total = service.list_urls(skip=skip, limit=limit)
    return UrlListResponse(urls=urls, total=total)


@router.get("/{short_code}", response_model=UrlDetailResponse)
def get_url_details(
    short_code: str,
    session: Session = Depends(get_session),
):
    """Get details of a shortened URL."""
    service = UrlService(session)
    return service.get_url_details(short_code)


@router.get("/{short_code}/stats", response_model=AnalyticsSummary)
def get_url_stats(
    short_code: str,
    session: Session = Depends(get_session),
):
     
    service = AnalyticsService(session)
    return service.get_analytics_summary(short_code)


@router.delete("/{short_code}", response_model=MessageResponse)
def deactivate_url(
    short_code: str,
    session: Session = Depends(get_session),
):
    
    service = UrlService(session)
    service.deactivate_url(short_code)
    return MessageResponse(message=f"Short URL '{short_code}' has been deactivated.")
