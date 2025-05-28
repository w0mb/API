from sqlalchemy import String, ForeignKey
from src.db import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column


class ComfortOrm(BaseOrm):
    __tablename__ = "comfort"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    
class RoomsComfortOrm(BaseOrm):
    __tablename__ = "rooms_comfort"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    rooms_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    comfort_id: Mapped[int] = mapped_column(ForeignKey("comfort.id"))