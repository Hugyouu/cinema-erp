from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Ticket
from app.schemas.ticket import TicketCreate, TicketRead

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.post("/", response_model=TicketRead, status_code=201)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = Ticket(**ticket.model_dump(), is_used=False)
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


@router.post("/{ticket_id}/validate", response_model=TicketRead)
def validate_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.is_used:
        raise HTTPException(status_code=400, detail="Ticket already used")
    ticket.is_used = True
    db.commit()
    db.refresh(ticket)
    return ticket
