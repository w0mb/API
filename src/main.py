from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as auth_router
from src.api.hotel import router as hotel_router
from src.config import settings
from src.db import *

app = FastAPI()
app.include_router(auth_router)
app.include_router(hotel_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8002)
