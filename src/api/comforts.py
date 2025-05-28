from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.chemas.comfort_chema import ComfortRequestAdd

router = APIRouter(prefix= "/comfort",tags=["Удобства комнат"])

@router.get("")
async def get_comforts(db: DBDep):
    return await db.comfort.get_all()

@router.post("")
async def add_comfort(db: DBDep, data: ComfortRequestAdd):
    added_data = await db.comfort.add_one(data)
    await db.commit()
    return {"status": "ok", "data": added_data}