from fastapi import Query, Body, APIRouter, Path
from src.api.dependencies import PaginationDep
from src.chemas.chema import hotel, hotelPatch, Config
from src.api.status import OK_JSON, NOTFOUND_JSON
from src.db import new_session

from sqlalchemy import insert, select
from src.models.hotel_models import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])

HOTEL_EXAMPLES = Config.schema_extra["examples"]


@router.get("")
async def get_hotels(pagination: PaginationDep,
                     title: str | None = Query(None, description="Название отеля"),
                     location:str | None = Query(None, description="Адрес отеля")):


    async with new_session() as session:
        query = select(HotelsOrm)

        result = await session.execute(query)
        hotels = result.scalars().all()
        print("Hotels without filters:", hotels)
        if title:
            hotels = [h for h in hotels if title.lower() in h.title.lower()]
        if location:
            hotels = [h for h in hotels if location.lower() in h.location.lower()]


        start = (pagination.page - 1) * pagination.count_ipp
        end = start + pagination.count_ipp
        hotels = hotels[start:end]
        return hotels


@router.post("/{hotel_id}")
async def add_hotel(hotel_data: hotel = Body(openapi_examples=HOTEL_EXAMPLES)):
    async with new_session() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return OK_JSON


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int = Path(description="ID отеля для удаления", example=1)):
    global hotels
    hotel_to_remove = next((hotel for hotel in hotels if hotel["id"] == hotel_id), None)
    if hotel_to_remove:
        hotels.remove(hotel_to_remove)
        return OK_JSON
    else:
        return NOTFOUND_JSON


@router.put("/{hotel_id}")
def change_hotel_put(hotel_id: int = Path(description="ID отеля для Полного изменения", example=1), hotel_data: hotel = Body(examples=HOTEL_EXAMPLES)):
    global hotels
    for hotel_item in hotels:
        if hotel_item["id"] == hotel_id:
            hotel_item["title"] = hotel_data.title
            hotel_item["rate"] = hotel_data.rate
            return OK_JSON
    return NOTFOUND_JSON


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
