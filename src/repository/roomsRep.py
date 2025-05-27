from sqlalchemy import select, func
from datetime import date

from src.models.rooms_models import RoomsOrm
from src.repository.baseRep import BaseRepository
from src.chemas.rooms_chema import Room
from src.models.boking_model import BookingOrm
from src.db import engine
from src.repository.utils import rooms_ids_for_booking
class RoomRepository(BaseRepository):
    model = RoomsOrm
    chema = Room
    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        return await self.get_filtred(RoomsOrm.id.in_(rooms_ids_to_get))