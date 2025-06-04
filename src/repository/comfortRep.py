from sqlalchemy import select, insert, delete

from src.repository.baseRep import BaseRepository
from src.models.comfort_model import ComfortOrm, RoomsComfortOrm
from src.chemas.comfort_chema import Comfort, RoomsComfort


class ComfortRepository(BaseRepository):
    model = ComfortOrm
    chema = Comfort
    
class RoomsComfortRepositiry(BaseRepository):
    model = RoomsComfortOrm
    chema = RoomsComfort

    async def set_room_comforts(self, rooms_id: int, comfort_ids: list[int]) -> None:
        get_current_comfort_ids_query = (
            select(self.model.comfort_id)
            .filter_by(rooms_id=rooms_id)
        )
        res = await self.session.execute(get_current_comfort_ids_query)
        current_comfort_ids: list[int] = res.scalars().all()
        ids_to_delete: list[int] = list(set(current_comfort_ids) - set(comfort_ids))
        ids_to_insert: list[int] = list(set(comfort_ids) - set(current_comfort_ids))

        if ids_to_delete:
            delete_m2m_comfort_stmt = (
                delete(self.model)
                .filter(
                    self.model.rooms_id == rooms_id,
                    self.model.comfort_id.in_(ids_to_delete),
                )
            )
            await self.session.execute(delete_m2m_comfort_stmt)

        if ids_to_insert:
            insert_m2m_comfort_stmt = (
                insert(self.model)
                .values([{"rooms_id": rooms_id, "comfort_id": c_id} for c_id in ids_to_insert])
            )
            await self.session.execute(insert_m2m_comfort_stmt)