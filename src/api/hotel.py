from fastapi import Query, Body, APIRouter, Path
from datetime import date

from src.api.dependencies import PaginationDep
from src.chemas.chema import hotel, hotelAdd,hotelPatch, Config
from src.api.status import Status
from src.db import new_session
from src.models.hotel_models import HotelsOrm
from src.repository.baseRep import BaseRepository
from src.repository.hotelRep import HotelRepository
from src.api.dependencies import DBDep


router = APIRouter(prefix="/hotels", tags=["Отели"])

HOTEL_EXAMPLES = Config.schema_extra["examples"]


@router.get("/")
async def get_hotels(
    db:DBDep,
    date_from: date,
    date_to: date,
    title: str = None,
    location: str = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=limit,
        offset=offset
    )


@router.get("/{hotel_id", name="Получить один")
async def get_hotel_by_id(hotel_id: int):
    async with new_session() as session:
        return await HotelRepository(session).get_one_or_none(id=hotel_id)

@router.post("/{hotel_id}")
async def add_hotel(hotel_data: hotelAdd = Body(openapi_examples=HOTEL_EXAMPLES)):
    async with new_session() as session:
        print(hotel_data.model_dump_json()) 
        result = await HotelRepository(session).add_one(hotel_data)
        await session.commit()
        return result

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int = Path(description="ID отеля для удаления", example=1)):
    async with new_session() as session:
        result = await HotelRepository(session).delete(id=hotel_id)
        await session.commit()
        return Status.OK_JSON

# Полное изменение чего-то
# В контексте задачи меняем запись в БД по id отеля

@router.put("/{hotel_id}")
async def change_hotel_put(hotel_id: int = Path(description="ID отеля для Полного изменения", example=1),
                           hotel_data: hotelAdd = Body(examples=HOTEL_EXAMPLES)):

    async with new_session() as session:
        await HotelRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
        return Status.OK_JSON

@router.patch("/{hotel_id}")
async def partially_edit_hotel(hotel_data: hotelPatch,
                               hotel_id: int = Path(description="ID отеля для Частичного изменения", example=1)):

    async with new_session() as session:
        await HotelRepository(session).edit(hotel_data, id=hotel_id, exclude_unset=True)
        await session.commit()
        return Status.OK_JSON