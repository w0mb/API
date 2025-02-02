from sqlalchemy import select, insert

from src.api.status import Status

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add_one(self, **kwargs):
        add_hotel_stmt = insert(self.model).values(kwargs)
        await self.session.execute(add_hotel_stmt)
        return Status.OK_JSON
