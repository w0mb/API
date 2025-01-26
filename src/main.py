from fastapi import FastAPI
import uvicorn
from src.api.hotel import router as hotel_router
from src.config import settings

print(f"{settings.DB_NAME=}")

app = FastAPI()
app.include_router(hotel_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8004)
