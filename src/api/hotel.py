from fastapi import Query, Body, APIRouter, Path
from src.api.dependencies import PaginationDep
from src.chemas.chema import hotel, hotelPatch, Config
from src.api.status import Status
from src.db import new_session

from sqlalchemy import insert, select, delete, update
from src.models.hotel_models import HotelsOrm

from src.repository.baseRep import BaseRepository
from src.repository.hotelRep import HotelRepository
router = APIRouter(prefix="/hotels", tags=["Отели"])

HOTEL_EXAMPLES = Config.schema_extra["examples"]


@router.get("")
async def get_hotels(pagination: PaginationDep,
                     title: str | None = Query(None, description="Название отеля"),
                     location:str | None = Query(None, description="Адрес отеля")):

    async with new_session() as session:
        limit = pagination.count_ipp
        offset = (pagination.page - 1) * pagination.count_ipp

        return await HotelRepository(session).get_all(title=title,
                                                      location=location,
                                                      limit=limit,
                                                      offset=offset)



@router.post("/{hotel_id}")
async def add_hotel(hotel_data: hotel = Body(openapi_examples=HOTEL_EXAMPLES)):
    async with new_session() as session:
        result = await HotelRepository(session).add_one(title=hotel_data.title,
                                                        location=hotel_data.location)
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
                           hotel_data: hotel = Body(examples=HOTEL_EXAMPLES)):

    async with new_session() as session:
        result = await HotelRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
        return Status.OK_JSON

@router.patch("/{hotel_id}")
async def partially_edit_hotel(hotel_data: hotelPatch,
                               hotel_id: int = Path(description="ID отеля для Частичного изменения", example=1)):

    async with new_session() as session:
        if hotel_data.title:
            partially_update_hotel_stmt = (update(HotelsOrm).
                                           where(HotelsOrm.id == hotel_id).
                                           values(title=hotel_data.title))
        if hotel_data.location:
            partially_update_hotel_stmt = (update(HotelsOrm).
                                           where(HotelsOrm.id == hotel_id).
                                           values(location=hotel_data.location))
        else: return Status.ERROR_JSON

        await session.execute(partially_update_hotel_stmt)
        await session.commit()
        return Status.OK_JSON