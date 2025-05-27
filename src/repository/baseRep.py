from sqlalchemy import select, insert, delete, update

from src.api.status import Status

from pydantic import BaseModel

class BaseRepository:
    model = None
    chema: BaseModel = None

    def __init__(self, session):
        self.session = session
    async def get_filtred(self, *filters, limit: int = None, offset: int = None):
        query = select(self.model).where(*filters)
        
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
            
        result = await self.session.execute(query)
        return [self.schema.model_validate(row, from_attributes=True) for row in result.scalars().all()]
    
    async def get_all(self, *args, **kwargs):
        return await self.get_filtred()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None: return None
        return self.chema.model_validate(model, from_attributes=True)

    async def add_one(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.chema.model_validate(model, from_attributes=True)

    async def delete(self, **filter_by) -> None:
        print(filter_by)
        print(self.model)
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def edit(self,data: BaseModel,exclude_unset: bool = False,  **filter_by) -> None:
        edit_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(edit_stmt)


