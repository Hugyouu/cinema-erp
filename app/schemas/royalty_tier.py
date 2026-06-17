from pydantic import BaseModel, ConfigDict


class RoyaltyTierRead(BaseModel):
    id: int
    contract_id: int
    week_number: int | None = None
    percentage: float | None = None

    model_config = ConfigDict(from_attributes=True)


class RoyaltyTierCreate(BaseModel):
    contract_id: int
    week_number: int | None = None
    percentage: float | None = None


class RoyaltyTierUpdate(BaseModel):
    week_number: int | None = None
    percentage: float | None = None
