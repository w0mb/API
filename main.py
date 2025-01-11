from fastapi import FastAPI, Body, Query
import uvicorn

OK_JSON = {"status": "ok"}
NOTFOUND_JSON = {"status": "not found"}


app = FastAPI()
hotels = [
    {"id": 1, "title": "debil", "rate": "bad"},
    {"id": 2, "title": "debiliii", "rate": "cool"},
    {"id": 3, "title": "daun", "rate": "awesome"}
]


@app.get("/hotels")
def get_hotels():
    global hotels
    return hotels

@app.post("/hotels/{hotel_id}")
def add_hotel(title: str = Body(), rate: str = Body()):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": title, "rate": rate})
    return OK_JSON


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotel_to_remove = next((hotel for hotel in hotels if hotel["id"] == hotel_id), None)
    if hotel_to_remove:
        hotels.remove(hotel_to_remove)
        return OK_JSON
    else:
        return NOTFOUND_JSON


@app.put("/hotels/{hotel_id}")
def change_hotel_put(hotel_id: int, hotel_name: str = Body(), hotel_rate: str = Body()):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_name
            hotel["rate"] = hotel_rate
            return OK_JSON
    return NOTFOUND_JSON


@app.patch("/hotels/{hotel_id}")
def patch_hotel(hotel_id: int, hotel_update: str | None = Body(None), new_par: str | None = Body(None)):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_update in ["title", "rate"]:
                hotel[hotel_update] = new_par
                return OK_JSON
    return NOTFOUND_JSON


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8003)
