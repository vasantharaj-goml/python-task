from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.models.ticket import TicketPriority, TicketStatus
from app.schemas.ticket_schema import (
    DeleteTicketResponse,
    TicketCreate,
    TicketResponse,
    TicketUpdate
)
from app.services.ticket_service import ticket_service


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(ticket_data: TicketCreate):
    return ticket_service.create_ticket(ticket_data)


@router.get(
    "",
    response_model=list[TicketResponse]
)
def get_all_tickets(
    ticket_status: TicketStatus | None = Query(
        default=None,
        alias="status"
    ),
    priority: TicketPriority | None = Query(default=None)
):
    return ticket_service.get_all_tickets(
        ticket_status=ticket_status,
        priority=priority
    )


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket_by_id(ticket_id: UUID):
    ticket = ticket_service.get_ticket_by_id(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} was not found"
        )

    return ticket


@router.put(
    "/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket(
    ticket_id: UUID,
    ticket_data: TicketUpdate
):
    updated_ticket = ticket_service.update_ticket(
        ticket_id=ticket_id,
        ticket_data=ticket_data
    )

    if updated_ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} was not found"
        )

    return updated_ticket


@router.delete(
    "/{ticket_id}",
    response_model=DeleteTicketResponse
)
def delete_ticket(ticket_id: UUID):
    deleted = ticket_service.delete_ticket(ticket_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} was not found"
        )

    return DeleteTicketResponse(
        message="Ticket deleted successfully",
        ticket_id=ticket_id
    )