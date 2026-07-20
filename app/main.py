from fastapi import FastAPI

from app.api.ticket_routes import router as ticket_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="Ticket CRUD API for AI Service Desk"
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