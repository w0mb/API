from fastapi import APIRouter, Path

from src.chemas.booking_chema import BookingRequestAdd, BookingAdd
from src.api.dependencies import DBDep
from src.api.dependencies import UserDependecies

router = APIRouter(prefix="/bookings", tags=["Бронирование Номеров в отелях"])

@router.post("/create/{booking_id}")
async def create_booking(
    db: DBDep,
    user_id: UserDependecies,
    bookingRequestAdd: BookingRequestAdd,
    booking_id: int = Path()
    ):
    
    user_data = await db.users.get_one_or_none(id=user_id)
    
    room_data = await db.rooms.get_one_or_none(id=bookingRequestAdd.room_id)
    
    res = BookingAdd(user_id=user_data.id, price=room_data.price, **bookingRequestAdd.model_dump())
    print(res)
    res_data = await db.bookings.add_one(res)
    print("РЕЕЕС ДАТА-",res_data)
    await db.commit()
    
    return {"status": "ok", "data": res_data}