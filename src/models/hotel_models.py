from sqlalchemy import String
from src.db import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column


class HotelsOrm(BaseOrm):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column()