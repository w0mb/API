from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys
from pathlib import Path



sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()
    # При выключении/перезагрузке приложения


app = FastAPI(docs_url=None, lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_bookings)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app")
