import pytest
from pydantic import ValidationError

from app.models.ticket import TicketPriority, TicketStatus
from app.schemas.ticket_schema import TicketCreate, TicketUpdate
from app.services.ticket_service import TicketService


@pytest.fixture
def service():
    return TicketService()


def test_create_ticket_sets_open_status_and_persists(service, db_session):
    payload = TicketCreate(
        title="Login problem",
        description="User cannot log in",
        priority=TicketPriority.HIGH,
    )

    ticket = service.create_ticket(db_session, payload)

    assert ticket.title == "Login problem"
    assert ticket.status == TicketStatus.OPEN
    assert ticket.priority == TicketPriority.HIGH
    assert db_session.query(type(ticket)).count() == 1


def test_get_all_tickets_filters_by_status_and_priority(service, db_session):
    service.create_ticket(
        db_session,
        TicketCreate(title="First issue", description="One", priority=TicketPriority.HIGH),
    )
    service.create_ticket(
        db_session,
        TicketCreate(title="Second issue", description="Two", priority=TicketPriority.LOW),
    )

    filtered = service.get_all_tickets(
        db_session,
        ticket_status=TicketStatus.OPEN,
        priority=TicketPriority.HIGH,
    )

    assert len(filtered) == 1
    assert filtered[0].title == "First issue"


def test_update_and_delete_ticket(service, db_session):
    created = service.create_ticket(
        db_session,
        TicketCreate(title="Bug", description="Needs update", priority=TicketPriority.MEDIUM),
    )

    updated = service.update_ticket(
        db_session,
        created.id,
        TicketUpdate(title="Bug fixed", status=TicketStatus.IN_PROGRESS),
    )

    assert updated is not None
    assert updated.title == "Bug fixed"
    assert updated.status == TicketStatus.IN_PROGRESS

    deleted = service.delete_ticket(db_session, created.id)

    assert deleted is True
    assert service.get_ticket_by_id(db_session, created.id) is None


def test_ticket_create_schema_rejects_short_title():
    with pytest.raises(ValidationError):
        TicketCreate(title="Hi", description="Invalid title")
