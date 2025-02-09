from src.models.rooms_models import RoomsOrm
from src.repository.baseRep import BaseRepository

class RoomRepository(BaseRepository):
    model = RoomsOrm