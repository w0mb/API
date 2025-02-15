from src.models.hotel_models import HotelsOrm
from src.repository.baseRep import BaseRepository

from sqlalchemy import select, insert

from src.api.status import Status

from src.chemas.chema import hotel


class HotelRepository(BaseRepository):
    model = HotelsOrm
    chema = hotel
    async def get_all(self, title, location, limit, offset):
        query = select(HotelsOrm)

        if title:
            query = query.where(HotelsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.where(HotelsOrm.location.ilike(f"%{location}%"))


        query = query.limit(limit).offset(offset)


        result = await self.session.execute(query)
        return [hotel.model_validate(hotels, from_attributes=True) for hotels in result.scalars().all()]

    # async def add_one(self, title, location):
    #     add_hotel_stmt = insert(HotelsOrm).values(title=title, location=location).returning(HotelsOrm)
    #     result = await self.session.execute(add_hotel_stmt)
    #     inserted_data = result.mappings().first()
    #     return Status.ok_with_data(dict(inserted_data))