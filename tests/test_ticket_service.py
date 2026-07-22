from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.models.ticket import TicketPriority, TicketStatus
from app.schemas.ticket_schema import TicketCreate, TicketUpdate
from app.services.ticket_service import TicketService


@pytest.fixture
def service():
    """Creates a fresh service object for every test."""
    return TicketService()


def sample_ticket(service: TicketService):
    """Helper function to create a ticket."""
    return service.create_ticket(
        TicketCreate(
            title="Login problem",
            description="User cannot log in",
            priority=TicketPriority.HIGH
        )
    )


# ---------------------------------------------------------
# 1. CREATE TICKET
# ---------------------------------------------------------

def test_create_ticket_positive(service):
    ticket_data = TicketCreate(
        title="Login problem",
        description="User cannot log in",
        priority=TicketPriority.HIGH
    )

    ticket = service.create_ticket(ticket_data)

    assert ticket.title == "Login problem"
    assert ticket.status == TicketStatus.OPEN
    assert ticket.priority == TicketPriority.HIGH


def test_create_ticket_negative():
    # Title must contain at least 3 characters
    with pytest.raises(ValidationError):
        TicketCreate(
            title="Hi",
            description="Invalid title"
        )

