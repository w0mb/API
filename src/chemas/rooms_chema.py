from pydantic import BaseModel

from src.chemas.comfort_chema import Comfort

class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    discription: str | None = None
    price: int
    count: int

class RoomRequestAdd(BaseModel):
    title: str
    discription: str | None = None
    price: int
    count: int
    comfort_ids: list[int] = []

class Room(RoomAdd):
    id: int

class RoomPatchRequest(BaseModel):
    title: str | None = None
    discription: str | None = None
    price: int | None = None
    count: int | None = None
    comfort_ids: list[int] = []
class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    discription: str | None = None
    price: int | None = None
    count: int | None = None
    
class RoomWithRels(Room):
    comforts: list[Comfort]