from datetime import date
from models.rooms_models import RoomsOrm
from src.models.hotel_models import HotelsOrm
from src.repository.baseRep import BaseRepository

from sqlalchemy import select, insert, func

from src.api.status import Status
from src.repository.utils import rooms_ids_for_booking
from src.chemas.chema import hotel


class HotelRepository(BaseRepository):
    model = HotelsOrm
    chema = hotel


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location,
            title,
            limit,
            offset,
    ) -> list[hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [hotel.model_validate(Hotel, from_attributes=True) for Hotel in result.scalars().all()]