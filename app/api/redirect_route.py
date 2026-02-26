from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.db.db import get_session
from app.services.url_service import UrlService
from app.services.analytics_service import AnalyticsService

router = APIRouter(tags=["Redirect"])


@router.get("/{short_code}")
async def redirect_to_url(
    short_code: str,
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    
    
    url_service = UrlService(session)
    url = url_service.resolve_url(short_code)

    # Record analytics in background
    analytics_service = AnalyticsService(session)

    # Extract request metadata
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    referrer = request.headers.get("referer")

    background_tasks.add_task(
        analytics_service.record_click,
        url_id=url.id,
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer,
    )

    return RedirectResponse(url=url.original_url, status_code=307)
