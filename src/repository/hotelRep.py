from src.models.hotel_models import HotelsOrm
from src.repository.baseRep import BaseRepository

from sqlalchemy import select, insert, delete, update

from src.api.status import Status
class HotelRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, title, location, limit, offset):
        query = select(HotelsOrm)

        if title:
            query = query.where(HotelsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.where(HotelsOrm.location.ilike(f"%{location}%"))


        query = query.limit(limit).offset(offset)


        result = await self.session.execute(query)
        hotels = result.scalars().all()

        return hotels

    async def add_one(self, title, location):
        add_hotel_stmt = insert(HotelsOrm).values(title=title, location=location).returning(HotelsOrm)
        result = await self.session.execute(add_hotel_stmt)
        inserted_data = result.mappings().first()
        return Status.ok_with_data(dict(inserted_data))

    async def delete(self, id) -> None:
        delete_hotel_stmt = delete(HotelsOrm).filter_by(id=id)
        await self.session.execute(delete_hotel_stmt)

    async def edit(self, id, title, location) -> None:
        update_hotel_stmt = update(HotelsOrm).filter_by(id=id).values(title=title, location=location)
        await self.session.execute(update_hotel_stmt)
