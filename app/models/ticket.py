from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Ticket(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    priority: TicketPriority
    status: TicketStatus
    created_at: datetime
    updated_at: datetime