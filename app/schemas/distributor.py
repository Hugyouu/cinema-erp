from pydantic import BaseModel, ConfigDict


class DistributorRead(BaseModel):
    id: int
    name: str
    country: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DistributorCreate(BaseModel):
    name: str
    country: str | None = None


class DistributorUpdate(BaseModel):
    name: str | None = None
    country: str | None = None
