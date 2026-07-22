from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.ticket_routes import router as ticket_router
from app.core.config import settings
from app.core.database import Base, engine

# Importing the model registers the tickets table
from app.models.ticket import Ticket  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="Ticket CRUD API for AI Service Desk",
    lifespan=lifespan
)


app.include_router(ticket_router)


@app.get("/", tags=["Root"])
def home():
    return {
        "message": f"{settings.app_name} is running",
        "version": settings.app_version,
        "documentation": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy"
    }