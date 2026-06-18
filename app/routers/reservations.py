import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Reservation, ResStatus, Seance, SeanceStatus
from app.schemas.reservation import ReservationCreate, ReservationRead

router = APIRouter(prefix="/reservations", tags=["Réservations"])


@router.get("/", response_model=list[ReservationRead])
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()


@router.get("/{reservation_id}", response_model=ReservationRead)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


@router.post("/", response_model=ReservationRead, status_code=201)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    seance = db.query(Seance).filter(Seance.id == reservation.seance_id).first()
    if not seance:
        raise HTTPException(status_code=404, detail="Séance not found")
    if seance.status == SeanceStatus.FULL:
        raise HTTPException(status_code=409, detail="Séance is full")
    if seance.status == SeanceStatus.CANCELLED:
        raise HTTPException(status_code=409, detail="Séance is cancelled")
    new_reservation = Reservation(
        **reservation.model_dump(),
        booking_ref=str(uuid.uuid4())[:8].upper(),
        status=ResStatus.PENDING,
        booked_at=datetime.now(timezone.utc),
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation


@router.post("/{reservation_id}/confirm", response_model=ReservationRead)
def confirm_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.status != ResStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending reservations can be confirmed")
    reservation.status = ResStatus.CONFIRMED

    seance = reservation.seance
    seance.seats_sold = (seance.seats_sold or 0) + 1
    if seance.seats_sold >= seance.room.capacity:
        seance.status = SeanceStatus.FULL

    db.commit()
    db.refresh(reservation)
    return reservation


@router.post("/{reservation_id}/cancel", response_model=ReservationRead)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.status in (ResStatus.CANCELLED, ResStatus.USED):
        raise HTTPException(status_code=400, detail=f"Reservation is already {reservation.status.value}")

    if reservation.status == ResStatus.CONFIRMED:
        seance = reservation.seance
        seance.seats_sold = max(0, (seance.seats_sold or 0) - 1)
        if seance.status == SeanceStatus.FULL:
            seance.status = SeanceStatus.OPEN

    reservation.status = ResStatus.CANCELLED
    db.commit()
    db.refresh(reservation)
    return reservation
