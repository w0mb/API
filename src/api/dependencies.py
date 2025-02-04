from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    count_ipp: Annotated[int | None, Query(2, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]