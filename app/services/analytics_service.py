from sqlmodel import Session
import uuid

from app.models.click_analytics import ClickAnalytics
from app.repostries.analytics_repository import AnalyticsRepository
from app.repostries.url_repository import UrlRepository
from app.core.user_agent_parser import parse_user_agent
from app.core.geo_lookup import get_geo_info
from app.schema.analytics_schema import (
    AnalyticsSummary,
    ClickDetail,
    BrowserStat,
    DeviceStat,
    CountryStat,
)


class AnalyticsService:

    def __init__(self, session: Session):
        self.analytics_repo = AnalyticsRepository(session)
        self.url_repo = UrlRepository(session)

    async def record_click(
        self,
        url_id: uuid.UUID,
        ip_address: str | None = None,
        user_agent: str | None = None,
        referrer: str | None = None,
    ) -> ClickAnalytics:
        # Parse user agent
        ua_info = parse_user_agent(user_agent or "")

        # Geo lookup
        geo_info = await get_geo_info(ip_address or "")

        click = ClickAnalytics(
            url_id=url_id,
            ip_address=ip_address,
            country=geo_info.get("country"),
            city=geo_info.get("city"),
            browser=ua_info.get("browser"),
            os=ua_info.get("os"),
            device_type=ua_info.get("device_type"),
            referrer=referrer,
        )

        created = self.analytics_repo.create_click(click)

        # Increment click count on the URL
        self.url_repo.increment_click_count(url_id)

        return created

    def get_analytics_summary(self, short_code: str) -> AnalyticsSummary:
        url = self.url_repo.get_by_short_code(short_code)
        if not url:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Short URL not found.")

        total_clicks = self.analytics_repo.count_clicks_by_url_id(url.id)

        # Browser stats
        browser_raw = self.analytics_repo.get_browser_stats(url.id)
        browsers = [
            BrowserStat(
                browser=name,
                count=count,
                percentage=round((count / total_clicks) * 100, 1) if total_clicks > 0 else 0,
            )
            for name, count in sorted(browser_raw.items(), key=lambda x: x[1], reverse=True)
        ]

        # Device stats
        device_raw = self.analytics_repo.get_device_stats(url.id)
        devices = [
            DeviceStat(
                device_type=name,
                count=count,
                percentage=round((count / total_clicks) * 100, 1) if total_clicks > 0 else 0,
            )
            for name, count in sorted(device_raw.items(), key=lambda x: x[1], reverse=True)
        ]

        # Country stats
        country_raw = self.analytics_repo.get_country_stats(url.id)
        countries = [
            CountryStat(
                country=name,
                count=count,
                percentage=round((count / total_clicks) * 100, 1) if total_clicks > 0 else 0,
            )
            for name, count in sorted(country_raw.items(), key=lambda x: x[1], reverse=True)
        ]

        # Recent clicks (last 20)
        recent_raw = self.analytics_repo.get_clicks_by_url_id(url.id, limit=20)
        recent_clicks = [
            ClickDetail(
                id=c.id,
                ip_address=c.ip_address,
                country=c.country,
                city=c.city,
                browser=c.browser,
                os=c.os,
                device_type=c.device_type,
                referrer=c.referrer,
                clicked_at=c.clicked_at,
            )
            for c in recent_raw
        ]

        return AnalyticsSummary(
            short_code=url.short_code,
            original_url=url.original_url,
            total_clicks=total_clicks,
            browsers=browsers,
            devices=devices,
            countries=countries,
            recent_clicks=recent_clicks,
        )
