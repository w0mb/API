import pytest
from tests.conftest import get_db_null_pool


async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert "data" in res
@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete_all()
        await _db.commit()

@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms",
    [
        (1, "2024-08-01", "2024-08-10", 1),
        (1, "2024-08-02", "2024-08-11", 2),
        (1, "2024-08-03", "2024-08-12", 3),
    ],
)
async def  test_add_and_get_bookings(
    db,
    room_id,
    date_from,
    date_to,
    booked_rooms,
    delete_all_bookings,
    authenticated_ac,
):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200
    response_my_bookings = await authenticated_ac.get("/bookings/me")
    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == booked_rooms
