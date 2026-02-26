from sqlmodel import Session, select
from app.models.click_analytics import ClickAnalytics
from typing import Optional
import uuid


class AnalyticsRepository:

    def __init__(self, session: Session):
        self.session = session

    def create_click(self, click: ClickAnalytics) -> ClickAnalytics:
        self.session.add(click)
        self.session.commit()
        self.session.refresh(click)
        return click

    def get_clicks_by_url_id(
        self, url_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> list[ClickAnalytics]:
        statement = (
            select(ClickAnalytics)
            .where(ClickAnalytics.url_id == url_id)
            .order_by(ClickAnalytics.clicked_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.session.exec(statement).all())

    def count_clicks_by_url_id(self, url_id: uuid.UUID) -> int:
        statement = select(ClickAnalytics).where(ClickAnalytics.url_id == url_id)
        return len(list(self.session.exec(statement).all()))

    def get_browser_stats(self, url_id: uuid.UUID) -> dict[str, int]:
        clicks = self.get_clicks_by_url_id(url_id, limit=10000)
        stats: dict[str, int] = {}
        for click in clicks:
            browser = click.browser or "Unknown"
            stats[browser] = stats.get(browser, 0) + 1
        return stats

    def get_device_stats(self, url_id: uuid.UUID) -> dict[str, int]:
        clicks = self.get_clicks_by_url_id(url_id, limit=10000)
        stats: dict[str, int] = {}
        for click in clicks:
            device = click.device_type or "Unknown"
            stats[device] = stats.get(device, 0) + 1
        return stats

    def get_country_stats(self, url_id: uuid.UUID) -> dict[str, int]:
        clicks = self.get_clicks_by_url_id(url_id, limit=10000)
        stats: dict[str, int] = {}
        for click in clicks:
            country = click.country or "Unknown"
            stats[country] = stats.get(country, 0) + 1
        return stats
