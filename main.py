from fastapi import FastAPI
import uvicorn

app = FastAPI()
hotels = [
    {"id": 1, "title":"debil", "rate": "bad"},
    {"id": 2, "title":"debiliii", "rate": "cool"},
    {"id": 3, "title":"daun", "rate": "awesome"}
]


@app.get("/hotels")
def get_hotels(hotel_name: str):
    return [hotel for hotel in hotels if hotel["title"] == hotel_name]

@app.put("/hotels/{hotel_id}")
def change_hotel_put(hotel_id: int, hotel_name: str, hotel_rate: str):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_name
            hotel["rate"] = hotel_rate
            return hotels

@app.patch("/hotels/{hotel_id}")
def patch_hotel(hotel_id: int, hotel_update: str, new_par: str):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
             for hotel in hotels:
                 if hotel_update in ["title", "rate"]:
                     hotel[hotel_update] = new_par
    return hotels



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8003)
