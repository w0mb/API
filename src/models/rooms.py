

import typing
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base

if typing.TYPE_CHEKING:
    from src.models.facilities import FacilitiesOrm


class RoomsOrm(Base):
    __tablename__ = "rooms"
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    facilities: Mapped[list["FacilitiesOrm"]] = relationship(
        back_populates="rooms",
        secondary="rooms_facilities",
    )
