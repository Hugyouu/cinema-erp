from pydantic import BaseModel, ConfigDict


class TicketRead(BaseModel):
    id: int
    reservation_id: int
    ticket_type: str | None = None
    seat_number: str | None = None
    unit_price: float | None = None
    is_used: bool

    model_config = ConfigDict(from_attributes=True)


class TicketCreate(BaseModel):
    reservation_id: int
    ticket_type: str | None = None
    seat_number: str | None = None
    unit_price: float | None = None


class TicketUpdate(BaseModel):
    ticket_type: str | None = None
    seat_number: str | None = None
    unit_price: float | None = None
    is_used: bool | None = None
