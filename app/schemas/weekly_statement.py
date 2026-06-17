from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models import StatementStatus


class WeeklyStatementRead(BaseModel):
    id: int
    contract_id: int
    week_start: date
    week_end: date
    gross_revenue: float | None = None
    royalty_rate: float | None = None
    royalty_amount: float | None = None
    status: StatementStatus | None = None
    generated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class WeeklyStatementCreate(BaseModel):
    contract_id: int
    week_start: date
    week_end: date
    gross_revenue: float | None = None
    royalty_rate: float | None = None
    royalty_amount: float | None = None
    status: StatementStatus | None = None


class WeeklyStatementUpdate(BaseModel):
    gross_revenue: float | None = None
    royalty_rate: float | None = None
    royalty_amount: float | None = None
    status: StatementStatus | None = None
