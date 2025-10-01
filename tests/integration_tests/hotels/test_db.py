from datetime import date

from src.database import async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from src.schemas.bookings import BookingAdd, BookingEdit

# async def test_add_hotel():
#     hotel_data = HotelAdd(title="Hotel 5 stars", location="Сочи")
#     async with DBManager(session_factory=async_session_maker_null_pool) as db:
#         new_hotel_data = await db.hotels.add(hotel_data)
#         await db.commit()

async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data_add = BookingAdd(
        user_id = user_id,
        room_id = room_id,
        date_from = date(year=2024, month=8, day=10),
        date_to = date(year=2024, month=8, day=20),
        price = 1000
    )
    booking_data_edit = BookingEdit(
        date_to = date(year=2024, month=8, day=22)
    )

    res_add = await db.bookings.add(booking_data_add)
    res_get = await db.bookings.get_one_or_none(id=res_add.id)

    assert res_add
    assert res_add.id == res_get.id
    assert res_add.room_id == res_get.room_id
    assert res_add.user_id == res_get.user_id

    await db.bookings.edit(booking_data_edit, True, id=res_add.id)
    updated_booking = await db.bookings.get_one_or_none(id=res_get.id)

    assert updated_booking
    assert updated_booking.id == res_get.id
    assert updated_booking.date_to == booking_data_edit.date_to

    await db.bookings.delete(id=res_get.id)
    booking = await db.bookings.get_one_or_none(id=res_get.id)
    assert not booking

    await db.commit()