from pydantic import BaseModel, ConfigDict

from app.models import RoomType


class RoomRead(BaseModel):
    id: int
    name: str
    capacity: int
    type: RoomType
        
    model_config = ConfigDict(from_attributes=True)

class RoomCreate(BaseModel):
    name: str
    capacity: int
    type: RoomType

class RoomUpdate(BaseModel):
    name: str | None = None
    capacity: int | None = None
    type: RoomType | None = None