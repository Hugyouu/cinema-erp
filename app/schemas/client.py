from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ClientRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    birth_date: date | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    birth_date: date | None = None


class ClientUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    birth_date: date | None = None
