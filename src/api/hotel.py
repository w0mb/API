from fastapi import Query, Body, APIRouter, Path
from src.api.dependencies import PaginationDep
from src.chemas.chema import hotel, hotelPatch, Config
from src.api.status import OK_JSON, NOTFOUND_JSON
from src.db import new_session

from sqlalchemy import insert, select, delete, update
from src.models.hotel_models import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])

HOTEL_EXAMPLES = Config.schema_extra["examples"]


@router.get("")
async def get_hotels(pagination: PaginationDep,
                     title: str | None = Query(None, description="Название отеля"),
                     location:str | None = Query(None, description="Адрес отеля")):


    async with new_session() as session:
        limit = pagination.count_ipp
        offset = (pagination.page - 1) * pagination.count_ipp


        query = select(HotelsOrm)

        if title:
            query = query.where(HotelsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.where(HotelsOrm.location.ilike(f"%{location}%"))


        query = query.limit(limit).offset(offset)


        result = await session.execute(query)
        hotels = result.scalars().all()

        return hotels


@router.post("/{hotel_id}")
async def add_hotel(hotel_data: hotel = Body(openapi_examples=HOTEL_EXAMPLES)):
    async with new_session() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
        return OK_JSON


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int = Path(description="ID отеля для удаления", example=1)):
    async with new_session() as session:
        delete_hotel_stmt = delete(HotelsOrm).where(HotelsOrm.id == hotel_id)
        await session.execute(delete_hotel_stmt)
        await session.commit()
        return OK_JSON

# Полное изменение чего-то
# В контексте задачи меняем запись в БД по id отеля
@router.put("/{hotel_id}")
async def change_hotel_put(hotel_id: int = Path(description="ID отеля для Полного изменения", example=1), hotel_data: hotel = Body(examples=HOTEL_EXAMPLES)):
    async with new_session() as session:
        update_hotel_stmt = (update(HotelsOrm).
                             where(HotelsOrm.id==hotel_id).
                             values(title=hotel_data.title, location=hotel_data.location))


        await session.execute(update_hotel_stmt)
        await session.commit()
        return OK_JSON


@router.patch("/{hotel_id}")
def partially_edit_hotel(hotel_data: hotelPatch, hotel_id: int = Path(description="ID отеля для Частичного изменения", example=1)):
    global hotels
    hotel_item = next((hotel for hotel in hotels if hotel["id"] == hotel_id), None)
    if not hotel_item:
        return NOTFOUND_JSON

    if hotel_data.title:
        hotel_item["title"] = hotel_data.title
    if hotel_data.name:
        hotel_item["name"] = hotel_data.name
    return OK_JSON
