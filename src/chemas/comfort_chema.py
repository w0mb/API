from pydantic import BaseModel, ConfigDict

class ComfortRequestAdd(BaseModel):
    title: str

class Comfort(ComfortRequestAdd):
    id: int
    
class RoomsComfortRequestAdd(BaseModel):
    rooms_id: int
    comfort_id: int
    
class RoomsComfort(RoomsComfortRequestAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)