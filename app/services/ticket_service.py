from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.models.ticket import Ticket, TicketPriority, TicketStatus
from app.schemas.ticket_schema import TicketCreate, TicketUpdate


class TicketService:

    def __init__(self) -> None:
        # Temporary in-memory database
        self.tickets: dict[UUID, Ticket] = {}

    def create_ticket(self, ticket_data: TicketCreate) -> Ticket:
        current_time = datetime.now(timezone.utc)

        new_ticket = Ticket(
            id=uuid4(),
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
            status=TicketStatus.OPEN,
            created_at=current_time,
            updated_at=current_time
        )

        self.tickets[new_ticket.id] = new_ticket

        return new_ticket

    def get_all_tickets(
        self,
        ticket_status: TicketStatus | None = None,
        priority: TicketPriority | None = None
    ) -> list[Ticket]:

        ticket_list = list(self.tickets.values())

        if ticket_status is not None:
            ticket_list = [
                ticket
                for ticket in ticket_list
                if ticket.status == ticket_status
            ]

        if priority is not None:
            ticket_list = [
                ticket
                for ticket in ticket_list
                if ticket.priority == priority
            ]

        return ticket_list

    def get_ticket_by_id(self, ticket_id: UUID) -> Ticket | None:
        return self.tickets.get(ticket_id)

    def update_ticket(
        self,
        ticket_id: UUID,
        ticket_data: TicketUpdate
    ) -> Ticket | None:

        existing_ticket = self.tickets.get(ticket_id)

        if existing_ticket is None:
            return None

        update_values = ticket_data.model_dump(exclude_unset=True)

        updated_ticket = existing_ticket.model_copy(
            update={
                **update_values,
                "updated_at": datetime.now(timezone.utc)
            }
        )

        self.tickets[ticket_id] = updated_ticket

        return updated_ticket

    def delete_ticket(self, ticket_id: UUID) -> bool:
        existing_ticket = self.tickets.get(ticket_id)

        if existing_ticket is None:
            return False

        del self.tickets[ticket_id]

        return True


# One shared service object
ticket_service = TicketService()