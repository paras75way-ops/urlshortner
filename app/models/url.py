from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List,TYPE_CHECKING
import uuid
if TYPE_CHECKING:
    from app.models.click_analytics import ClickAnalytics


class Url(SQLModel, table=True):
    __tablename__ = "urls"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    short_code: str = Field(index=True, unique=True, max_length=20)
    original_url: str = Field(max_length=2048)
    custom_alias: Optional[str] = Field(default=None, max_length=50)
    title: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    click_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = Field(default=None)

    # Relationship
    clicks: List["ClickAnalytics"] = Relationship(back_populates="url",sa_relationship_kwargs={"cascade": "all, delete-orphan"})
