



async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        }
    )

    assert response.status_code == 200

async def test_facilities(ac):
    response_add = await ac.post(
        "/facilities",
        json={
            "title": "Душ"
        }
    )

    response_get = await ac.get("/facilities")


    assert response_add.status_code == 200
    facility_titles = [facility["title"] for facility in response_get.json()]
    assert "Душ" in facility_titles

    assert response_get.status_code == 200
    assert isinstance(response_get.json(), list)

