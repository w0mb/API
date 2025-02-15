from fastapi import APIRouter
from passlib.context import CryptContext

from src.chemas.chema import UserRequestAdd, UserAdd
from src.db import new_session
from src.repository.userRep import UserRepository
from src.api.status import Status
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/users", tags=["Авторизация и Аунтефикация пользователей"])

@router.post("/")
async def add_user(data: UserRequestAdd):
    async with new_session() as session:
        hashed_password = pwd_context.hash(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await UserRepository(session).add_one(new_user_data)
        await session.commit()
        return Status.OK_JSON
