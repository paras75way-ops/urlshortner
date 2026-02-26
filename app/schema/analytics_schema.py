from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class ClickDetail(BaseModel):
    id: uuid.UUID
    ip_address: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    device_type: Optional[str] = None
    referrer: Optional[str] = None
    clicked_at: datetime


class BrowserStat(BaseModel):
    browser: str
    count: int
    percentage: float


class DeviceStat(BaseModel):
    device_type: str
    count: int
    percentage: float


class CountryStat(BaseModel):
    country: str
    count: int
    percentage: float


class AnalyticsSummary(BaseModel):
    short_code: str
    original_url: str
    total_clicks: int
    browsers: list[BrowserStat]
    devices: list[DeviceStat]
    countries: list[CountryStat]
    recent_clicks: list[ClickDetail]
