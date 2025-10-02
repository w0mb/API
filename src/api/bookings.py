from datetime import date
from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def create_booking(
    db: DBDep,
    hotel_id: int,
    date_from: date,
    date_to: date,
):
    booking = await db.bookings.add_booking(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )
    return {"status": "Ok", "data": booking}
