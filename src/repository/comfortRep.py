from src.repository.baseRep import BaseRepository
from src.models.comfort_model import ComfortOrm, RoomsComfortOrm
from src.chemas.comfort_chema import Comfort, RoomsComfort


class ComfortRepository(BaseRepository):
    model = ComfortOrm
    chema = Comfort
    
class RoomsComfortRepositiry(BaseRepository):
    model = RoomsComfortOrm
    chema = RoomsComfort
