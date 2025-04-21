from src.models.rooms_models import RoomsOrm
from src.repository.baseRep import BaseRepository
from src.chemas.rooms_chema import Room

class RoomRepository(BaseRepository):
    model = RoomsOrm
    chema = Room