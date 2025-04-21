from fastapi import Query, Body, APIRouter, Path
from src.api.dependencies import PaginationDep
from src.chemas.chema import hotel, hotelAdd, hotelPatch, Config
from src.chemas.rooms_chema import Room, RoomAdd, RoomPatch
from src.api.status import Status
from src.db import new_session

from sqlalchemy import insert, select, delete, update
from src.models.hotel_models import HotelsOrm

from src.repository.baseRep import BaseRepository
from src.repository.hotelRep import HotelRepository
from src.repository.roomsRep import RoomRepository
router = APIRouter(prefix="/hotels", tags=["Номера"])

HOTEL_EXAMPLES = Config.schema_extra["examples"]


@router.get("/")
async def get_rooms():
    async with new_session() as session:
        return await RoomRepository(session).get_all()

@router.get("/{room_id}", name="Получить один")
async def get_room_by_id(room_id: int):
    print(room_id)
    async with new_session() as session:
        return await RoomRepository(session).get_one_or_none(id=room_id)

@router.post("/{hotel_id}/{room_id}")
async def add_rooms(room_data: RoomAdd = Body()):
    async with new_session() as session:
        print(room_data.model_dump_json()) 
        result = await RoomRepository(session).add_one(room_data)
        await session.commit()
        return result

@router.delete("/{hotel_id}/{room_id}")
async def delete_room(room_id: int = Path(description="ID комнаты для удаления", example=6)):
    async with new_session() as session:
        await RoomRepository(session).delete(id=room_id)
        await session.commit()
        return Status.OK_JSON

# Полное изменение чего-то
# В контексте задачи меняем запись в БД по id отеля

@router.put("/{hotel_id}/{room_id}")
async def change_room_put(room_id: int = Path(description="ID комнаты для Полного изменения", example=7),
                           room_data: RoomAdd = Body()):

    async with new_session() as session:
        await RoomRepository(session).edit(room_data, id=room_id)
        await session.commit()
        return Status.OK_JSON

@router.patch("/{hotel_id}/{room_id}")
async def partially_edit_room(room_data: RoomPatch,
                               room_id: int = Path(description="ID комнаты для Частичного изменения", example=7)):

    async with new_session() as session:
        await RoomRepository(session).edit(room_data, id=room_id, exclude_unset=True)
        await session.commit()
        return Status.OK_JSON