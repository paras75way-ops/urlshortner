from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from app.db.db import engine
from app.models import Url, ClickAnalytics  # noqa: F401 — register models
from app.api.url_routes import router as url_router
from app.api.redirect_route import router as redirect_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables (for dev; use Alembic in production)
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="URL Shortener",
    description="Backend service to shorten long URLs and manage redirections with analytics.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers — API routes first, then catch-all redirect
app.include_router(url_router)
app.include_router(redirect_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "URL Shortener"}