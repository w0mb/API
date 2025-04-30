from pydantic import BaseModel
from sqlalchemy import insert

from src.repository.baseRep import BaseRepository
from src.models.boking_model import BookingOrm
from src.chemas.booking_chema import Booking


class BookingRepository(BaseRepository):
    model = BookingOrm
    chema = Booking
    
    async def add_one(self, data: BaseModel):

        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)

        result = await self.session.execute(add_data_stmt)
        
        model = result.scalars().one()
        
        return self.chema.model_validate(model, from_attributes=True)
