from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models import SubPlan, SubStatus


class SubscriptionRead(BaseModel):
    id: int
    client_id: int
    plan: SubPlan
    price_monthly: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: SubStatus
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class SubscriptionCreate(BaseModel):
    plan: SubPlan
    price_monthly: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: SubStatus


class SubscriptionUpdate(BaseModel):
    plan: SubPlan | None = None
    price_monthly: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: SubStatus | None = None
