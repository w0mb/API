from pydantic import BaseModel
from datetime import date

class BookingRequestAdd(BaseModel):
    room_id:int
    date_from:date
    date_to:date

class BookingAdd(BookingRequestAdd):
    user_id: int
    price: int
class Booking(BookingAdd):
    id:int