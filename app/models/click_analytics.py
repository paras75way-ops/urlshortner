from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional,TYPE_CHECKING
import uuid
if TYPE_CHECKING:
    from app.models.url import Url
 


class ClickAnalytics(SQLModel, table=True):
    __tablename__ = "click_analytics"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    url_id: uuid.UUID = Field(foreign_key="urls.id", index=True)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    country: Optional[str] = Field(default=None, max_length=100)
    city: Optional[str] = Field(default=None, max_length=100)
    browser: Optional[str] = Field(default=None, max_length=100)
    os: Optional[str] = Field(default=None, max_length=100)
    device_type: Optional[str] = Field(default=None, max_length=20)  # mobile, desktop, tablet
    referrer: Optional[str] = Field(default=None, max_length=2048)
    clicked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship
    url: Optional["Url"] = Relationship(back_populates="clicks")
