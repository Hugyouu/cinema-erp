from pydantic import BaseModel, ConfigDict

from app.models import SeanceFormat, SeanceStatus


class SeanceRead(BaseModel):
    id: int
    film_id: int
    room_id: int
    start_at: str | None = None
    end_at: str | None = None
    format: SeanceFormat | None = None
    status: SeanceStatus | None = None
    seats_sold: int | None = None
        
    model_config = ConfigDict(from_attributes=True)

class SeanceCreate(BaseModel):
    film_id: int
    room_id: int
    start_at: str | None = None
    end_at: str | None = None
    format: SeanceFormat | None = None
    status: SeanceStatus | None = None
    # seats_sold: int | None = None
    
class SeanceUpdate(BaseModel):
    film_id: int | None = None
    room_id: int | None = None
    start_at: str | None = None
    end_at: str | None = None
    format: SeanceFormat | None = None
    status: SeanceStatus | None = None
    seats_sold: int | None = None