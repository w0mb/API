from datetime import datetime, timezone, timedelta

import jwt
from aiohttp.abc import HTTPException
from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext

from src.chemas.chema import UserRequestAdd, UserAdd
from src.db import new_session
from src.repository.userRep import UserRepository
from src.api.status import Status
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/users", tags=["Авторизация и Аунтефикация пользователей"])

SECRET_KEY = "4734eb9cc2ca88a726916784feef90f80e941bb07752dc9c7e56c38bb9bfc7a0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register")
async def add_user(data: UserRequestAdd):
    async with new_session() as session:
        hashed_password = pwd_context.hash(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await UserRepository(session).add_one(new_user_data)
        await session.commit()
        return Status.OK_JSON

@router.post("/login")
async def login_user(data: UserRequestAdd):
    async with new_session() as session:
        user = await UserRepository(session).get_user_with_hashed_pass(email=data.email)
        if not user: raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not verify_password(data.password, user.hashed_password): raise HTTPException(status_code=401, detail="Невернный пароль")
        return create_access_token({"user_id": user.id})




