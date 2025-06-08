from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import date

from src.models.rooms_models import RoomsOrm
from src.repository.baseRep import BaseRepository
from src.chemas.rooms_chema import Room, RoomWithRels
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
        
        query = (
            select(self.model).
            options(selectinload(self.model.comfort)).
            filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model) for model in result.unique().scalars().all()]