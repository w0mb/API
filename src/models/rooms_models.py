# rooms_models.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.db import BaseOrm

class RoomsOrm(BaseOrm):
    __tablename__ = "rooms"
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    # Используем backref вместо back_populates
    facilities = relationship(
        "FacilitiesOrm", 
        secondary="rooms_facilities",
        backref="rooms"  # Создаст автоматическое отношение в FacilitiesOrm
    )