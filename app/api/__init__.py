from app.api.ai_routes import router as ai_router
from app.api.ticket_routes import router as ticket_router

__all__ = [
    "ai_router",
    "ticket_router",
]