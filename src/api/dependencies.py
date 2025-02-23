from typing import Annotated
from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel

from src.service.AuthService import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    count_ipp: Annotated[int | None, Query(2, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get("acsess_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="нет токена")
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]

UserDependecies = Annotated[int, Depends(get_current_user_id)]