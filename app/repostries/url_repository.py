from sqlmodel import Session, select
from app.models.url import Url
from typing import Optional
import uuid


class UrlRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, url: Url) -> Url:
        self.session.add(url)
        self.session.commit()
        self.session.refresh(url)
        return url

    def get_by_short_code(self, short_code: str) -> Optional[Url]:
        statement = select(Url).where(Url.short_code == short_code)
        return self.session.exec(statement).first()

    def get_by_custom_alias(self, alias: str) -> Optional[Url]:
        statement = select(Url).where(Url.custom_alias == alias)
        return self.session.exec(statement).first()

    def get_all(self, skip: int = 0, limit: int = 50) -> list[Url]:
        statement = select(Url).order_by(Url.created_at.desc()).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def count_all(self) -> int:
        statement = select(Url)
        return len(list(self.session.exec(statement).all()))

    def deactivate(self, short_code: str) -> Optional[Url]:
        url = self.get_by_short_code(short_code)
        if url:
            url.is_active = False
            self.session.add(url)
            self.session.commit()
            self.session.refresh(url)
        return url

    def increment_click_count(self, url_id: uuid.UUID) -> None:
        statement = select(Url).where(Url.id == url_id)
        url = self.session.exec(statement).first()
        if url:
            url.click_count += 1
            self.session.add(url)
            self.session.commit()
