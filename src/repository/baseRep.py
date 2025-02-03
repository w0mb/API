from sqlalchemy import select, insert, delete, update

from src.api.status import Status

from src.chemas.chema import BaseModel

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

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def edit(self,data: BaseModel, **filter_by) -> None:
        edit_stmt = update(self.model).filter_by(**filter_by).values(data)
        await self.session.execute()


