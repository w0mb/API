from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import BaseOrm


class RoomsOrm(BaseOrm):
    __tablename__ = "rooms"
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    discription: Mapped[str | None]
    price: Mapped[int]
    count: Mapped[int]

    comfort: Mapped[list["ComfortOrm"]] = relationship( # type: ignore
        secondary="rooms_comfort",
        back_populates="rooms",
        
    )