from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy.orm import Session

from app.core.database import get_db
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
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db)
):
    return ticket_service.create_ticket(
        db=db,
        ticket_data=ticket_data
    )


@router.get(
    "",
    response_model=list[TicketResponse]
)
def get_all_tickets(
    ticket_status: TicketStatus | None = Query(
        default=None,
        alias="status"
    ),
    priority: TicketPriority | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return ticket_service.get_all_tickets(
        db=db,
        ticket_status=ticket_status,
        priority=priority
    )


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket_by_id(
    ticket_id: UUID,
    db: Session = Depends(get_db)
):
    ticket = ticket_service.get_ticket_by_id(
        db=db,
        ticket_id=ticket_id
    )

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
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db)
):
    updated_ticket = ticket_service.update_ticket(
        db=db,
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
def delete_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db)
):
    deleted = ticket_service.delete_ticket(
        db=db,
        ticket_id=ticket_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} was not found"
        )

    return DeleteTicketResponse(
        message="Ticket deleted successfully",
        ticket_id=ticket_id
    )