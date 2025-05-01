from fastapi import APIRouter, Path

from src.chemas.booking_chema import BookingRequestAdd, BookingAdd
from src.api.dependencies import DBDep
from src.api.dependencies import UserDependecies

router = APIRouter(prefix="/bookings", tags=["Бронирование Номеров в отелях"])

@router.post("/create/{booking_id}",
             name="Создать бронирование",
             description="Создает новое бронирование с помощью DBmanager\n\n"
             "Создавать бронь имеет право только аутентифицированный пользователь\n\n"
             "Получаем id такого пользователя через get_current_user_id из dependencies"
        )
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

@router.get("",
            name="Получить все бронирования",
            description="Возвращает все бронирования всех пользователей посредством DBmanager"
        )
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()

@router.get("/me",
            name="Получить бронирования у текущего пользователя",
            description="Возвращает все бронирования текущего пользователя посредством DBmanager\n\n"
            "и get_current_user_id из dependencies"
        )
async def get_my_bookings(db: DBDep, user_id: UserDependecies):
    return await db.bookings.get_filtred(user_id=user_id) 