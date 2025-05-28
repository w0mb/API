from pydantic import BaseModel

class ComfortRequestAdd(BaseModel):
    title: str

class Comfort(ComfortRequestAdd):
    id: int
    
class RoomsComfort(BaseModel):
    id: int
    rooms_id: int
    comfort_id: int