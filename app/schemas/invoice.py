from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models import InvoiceStatus


class InvoiceRead(BaseModel):
    id: int
    invoice_number: str
    distributor_id: int
    statement_id: int
    amount_ht: float | None = None
    amount_ttc: float | None = None
    issued_at: date | None = None
    due_date: date | None = None
    status: InvoiceStatus

    model_config = ConfigDict(from_attributes=True)


class InvoiceCreate(BaseModel):
    distributor_id: int
    statement_id: int
    amount_ht: float | None = None
    amount_ttc: float | None = None
    issued_at: date | None = None
    due_date: date | None = None
    status: InvoiceStatus


class InvoiceUpdate(BaseModel):
    amount_ht: float | None = None
    amount_ttc: float | None = None
    issued_at: date | None = None
    due_date: date | None = None
    status: InvoiceStatus | None = None
