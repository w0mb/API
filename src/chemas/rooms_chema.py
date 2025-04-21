from pydantic import BaseModel, Field

class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    discription: str | None
    price: int
    count: int

class Room(RoomAdd):
    id: int

class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    discription: str | None = Field(None)
    price: int | None = Field(None)
    count: int | None = Field(None)