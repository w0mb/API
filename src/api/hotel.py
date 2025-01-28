from fastapi import Query, Body, APIRouter, Path
from src.api.dependencies import PaginationDep
from src.chemas.chema import hotel, hotelPatch, Config
from src.api.status import OK_JSON, NOTFOUND_JSON

router = APIRouter(prefix="/hotels", tags=["Отели"])

HOTEL_EXAMPLES = Config.schema_extra["examples"]

hotels = [
    {"id": 1, "title": "debil", "rate": "bad"},
    {"id": 2, "title": "debiliii", "rate": "cool"},
    {"id": 3, "title": "daun", "rate": "awesome"},
    {"id": 4, "title": "genius", "rate": "good"},
    {"id": 5, "title": "smart", "rate": "excellent"},
    {"id": 6, "title": "intelligent", "rate": "amazing"},
]


@router.get("/")
def get_hotels(pagination: PaginationDep):
    global hotels
    start = (pagination.page - 1) * pagination.count_ipp
    end = start + pagination.count_ipp

    return {
        "page": pagination.page,
        "count_item_per_page": pagination.count_ipp,
        "data": hotels[start:end]
    }


@router.post("/{hotel_id}")
def add_hotel(hotel_data: hotel = Body(openapi_examples=HOTEL_EXAMPLES)):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": hotel_data.title, "rate": hotel_data.rate})
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
