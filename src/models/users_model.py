from sqlalchemy import String
from src.db import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column


class UsersOrm(BaseOrm):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
