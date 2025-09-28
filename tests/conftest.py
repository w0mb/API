import pytest, json

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.models import *
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.utils.db_manager import DBManager

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    await load_test_data_from_files()

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "1234"
            }
        )

async def load_test_data_from_files():    
    async with DBManager(async_session_maker) as db:
        with open("mock_hotels.json", 'r', encoding='utf-8') as file:
            hotels_data = json.load(file)

        for hotel_data in hotels_data:
            hotel_schema = HotelAdd(**hotel_data)
            await db.hotels.add(hotel_schema)

        with open("mock_rooms.json", 'r', encoding='utf-8') as file:
            rooms_data = json.load(file)
        
        for room_data in rooms_data:
            room_schema = RoomAdd(**room_data)
            await db.rooms.add(room_schema)
        
        await db.commit()