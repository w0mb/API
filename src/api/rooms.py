from datetime import date
from fastapi import Query, Body, APIRouter, Path
from src.api.dependencies import PaginationDep
from src.chemas.chema import hotel, hotelAdd, hotelPatch, Config
from src.chemas.rooms_chema import Room, RoomAdd, RoomPatch, RoomRequestAdd, RoomPatchRequest
from src.api.status import Status
from src.db import new_session
from src.chemas.comfort_chema import ComfortRequestAdd, RoomsComfortRequestAdd
from sqlalchemy import insert, select, delete, update
from src.models.hotel_models import HotelsOrm
from src.api.dependencies import DBDep
from src.repository.baseRep import BaseRepository
from src.repository.hotelRep import HotelRepository
from src.repository.roomsRep import RoomRepository
router = APIRouter(prefix="/hotels", tags=["Номера"])

HOTEL_EXAMPLES = Config.schema_extra["examples"]


@router.get("/{hotel_id}/rooms", name="Получить все комнаты у отеля")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10")
        ):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms/{room_id}", name="Получить одну комнату а отеля")
async def get_room_by_id(hotel_id: int, room_id: int):
    async with new_session() as session:
        return await RoomRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)

@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomRequestAdd = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add_one(_room_data)

    rooms_comfort_data = [RoomsComfortRequestAdd(rooms_id=room.id, comfort_id=comfort_id) for comfort_id in room_data.comfort_ids]
    await db.rooms_comfort.add_bulk(rooms_comfort_data)
    await db.commit()

    return {"status": "OK", "data": room}

@router.delete("/{hotel_id}/rooms/{room_id}", name="удалить комнату у отеля")
async def delete_room(
        hotel_id: int = Path(description="ID отеля, у которого удаляем комнату"),
        room_id: int = Path(description="ID комнаты для удаления", example=6)
    ):
    async with new_session() as session:
        await RoomRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
        return Status.OK_JSON

# Полное изменение чего-то
# В контексте задачи меняем запись в БД по id отеля

@router.put("/{hotel_id}/rooms/{room_id}", name="полностью изменить комнату у отеля")
async def change_room_put(
        db: DBDep,
        hotel_id: int = Path(description="ID отеля, у которого меняем комнату"),
        room_id: int = Path(description="ID комнаты для Полного изменения", example=7),
        room_data: RoomRequestAdd = Body()
    ):
    await db.rooms_comfort.delete(rooms_id=room_id)
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.edit(_room_data, id=room_id)

    rooms_comfort_data = [RoomsComfortRequestAdd(rooms_id=room_id, comfort_id=comfort_id) for comfort_id in room_data.comfort_ids]
    await db.rooms_comfort.add_bulk(rooms_comfort_data)
    await db.commit()

    return {"status": "OK", "data": room}

@router.patch("/{hotel_id}/rooms/{room_id}", name="частично поменять комнату у отеля")
async def partially_edit_room(
        db: DBDep,
        room_data: RoomPatchRequest,
        hotel_id: int = Path(description="ID отеля, у которого меняем комнату"),
        room_id: int = Path(description="ID комнаты для Частичного изменения", example=7)
    ):
    current_comforts = await db.rooms_comfort.get_filtred(rooms_id=room_id)
    # Извлекаем ID текущих удобств
    current_ids = {c.comfort_id for c in current_comforts}
    
    # Обрабатываем comfort_ids (поддерживаем int, list[int] и None)
    comfort_ids = room_data.comfort_ids
    if comfort_ids is None:
        comfort_ids = []
    elif isinstance(comfort_ids, int):
        comfort_ids = [comfort_ids]
    
    requested_ids = set(comfort_ids)
    
    # Находим только ID для добавления (новые связи)
    ids_to_add = requested_ids - current_ids
    
    # Массовое добавление новых связей
    if ids_to_add:
        to_add = [
            RoomsComfortRequestAdd(rooms_id=room_id, comfort_id=comfort_id)
            for comfort_id in ids_to_add
        ]
        await db.rooms_comfort.delete(rooms_id=room_id)
        await db.rooms_comfort.add_bulk(to_add)

    # Обновляем основную информацию о комнате - ВАЖНО: исключаем comfort_ids
    room_update_data = room_data.model_dump(exclude={"comfort_ids"}, exclude_unset=True)
    if room_update_data:
        _room_data = RoomPatch(id=room_id, hotel_id=hotel_id, **room_update_data)
        await db.rooms.edit(_room_data)
    
    await db.commit()
        
    