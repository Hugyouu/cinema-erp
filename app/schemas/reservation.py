from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import ResStatus


class ReservationRead(BaseModel):
    id: int
    seance_id: int
    client_id: int
    subscription_id: int | None = None
    booking_ref: str | None = None
    status: ResStatus
    total_amount: float | None = None
    booked_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ReservationCreate(BaseModel):
    seance_id: int
    client_id: int
    subscription_id: int | None = None
    total_amount: float | None = None


class ReservationUpdate(BaseModel):
    status: ResStatus | None = None
    total_amount: float | None = None
