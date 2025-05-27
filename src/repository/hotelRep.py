from datetime import date
from models.rooms_models import RoomsOrm
from src.models.hotel_models import HotelsOrm
from src.repository.baseRep import BaseRepository

from sqlalchemy import select, insert

from src.api.status import Status
from src.repository.utils import rooms_ids_for_booking
from src.chemas.chema import hotel


class HotelRepository(BaseRepository):
    model = HotelsOrm
    chema = hotel


    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        title: str = None,
        location: str = None,
        limit: int = None,
        offset: int = None
    ):
        # Получаем ID комнат через запрос к БД
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from, 
            date_to=date_to
        )
        
        # Если нет доступных комнат, возвращаем пустой список
        if not rooms_ids_to_get:
            return []
        
        # Формируем подзапрос для получения hotel_id
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        
        # Собираем фильтры
        filters = []
        filters.append(HotelsOrm.id.in_(hotels_ids_to_get))
        
        if title:
            filters.append(HotelsOrm.title.ilike(f"%{title}%"))  # Используем ilike
        
        if location:
            filters.append(HotelsOrm.location.ilike(f"%{location}%"))
        
        # Возвращаем результат с пагинацией
        return await self.get_filtred(
            *filters,
            limit=limit,
            offset=offset
        )