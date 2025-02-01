from sqlalchemy import String, ForeignKey
from src.db import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column


class RoomsOrm(BaseOrm):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    discription: Mapped[str | None]
    price: Mapped[int]
    count: Mapped[int]