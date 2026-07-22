from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket import (
    Ticket,
    TicketPriority,
    TicketStatus
)
from app.schemas.ticket_schema import TicketCreate, TicketUpdate


class TicketService:

    def create_ticket(
        self,
        db: Session,
        ticket_data: TicketCreate
    ) -> Ticket:

        new_ticket = Ticket(
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
            status=TicketStatus.OPEN
        )

        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)

        return new_ticket

    def get_all_tickets(
        self,
        db: Session,
        ticket_status: TicketStatus | None = None,
        priority: TicketPriority | None = None
    ) -> list[Ticket]:

        statement = select(Ticket)

        if ticket_status is not None:
            statement = statement.where(
                Ticket.status == ticket_status
            )

        if priority is not None:
            statement = statement.where(
                Ticket.priority == priority
            )

        statement = statement.order_by(
            Ticket.created_at.desc()
        )

        return list(db.scalars(statement).all())

    def get_ticket_by_id(
        self,
        db: Session,
        ticket_id: UUID
    ) -> Ticket | None:

        return db.get(Ticket, ticket_id)

    def update_ticket(
        self,
        db: Session,
        ticket_id: UUID,
        ticket_data: TicketUpdate
    ) -> Ticket | None:

        existing_ticket = db.get(Ticket, ticket_id)

        if existing_ticket is None:
            return None

        update_values = ticket_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_values.items():
            setattr(existing_ticket, field, value)

        existing_ticket.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(existing_ticket)

        return existing_ticket

    def delete_ticket(
        self,
        db: Session,
        ticket_id: UUID
    ) -> bool:

        existing_ticket = db.get(Ticket, ticket_id)

        if existing_ticket is None:
            return False

        db.delete(existing_ticket)
        db.commit()

        return True


ticket_service = TicketService()