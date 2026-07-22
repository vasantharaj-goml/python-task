from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket, TicketPriority, TicketStatus


class TicketRepository:
    """Read and write Ticket records using a SQLAlchemy session."""

    def create(self, db: Session, ticket: Ticket) -> Ticket:
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    def find_all(
        self,
        db: Session,
        ticket_status: TicketStatus | None = None,
        priority: TicketPriority | None = None,
    ) -> list[Ticket]:
        statement = select(Ticket)

        if ticket_status is not None:
            statement = statement.where(Ticket.status == ticket_status)

        if priority is not None:
            statement = statement.where(Ticket.priority == priority)

        statement = statement.order_by(Ticket.created_at.desc())
        return list(db.scalars(statement).all())

    def find_by_id(self, db: Session, ticket_id: UUID) -> Ticket | None:
        return db.get(Ticket, ticket_id)

    def update(
        self,
        db: Session,
        ticket: Ticket,
        update_values: dict[str, object],
    ) -> Ticket:
        for field, value in update_values.items():
            setattr(ticket, field, value)

        db.commit()
        db.refresh(ticket)
        return ticket

    def delete(self, db: Session, ticket: Ticket) -> None:
        db.delete(ticket)
        db.commit()


ticket_repository = TicketRepository()