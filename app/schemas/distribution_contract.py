from pydantic import BaseModel, ConfigDict


class DistributionContractRead(BaseModel):
    id: int
    film_id: int
    distributor_id: int
    start_at: str | None = None
    end_at: str | None = None
    status: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DistributionContractCreate(BaseModel):
    film_id: int
    distributor_id: int
    start_at: str | None = None
    end_at: str | None = None
    status: str | None = None


class DistributionContractUpdate(BaseModel):
    start_at: str | None = None
    end_at: str | None = None
    status: str | None = None
