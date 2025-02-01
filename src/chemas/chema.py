from pydantic import BaseModel, Field

class hotel(BaseModel):
    title: str
    location: str

class hotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)

class Config:
    schema_extra = {
        "examples": {
            "1": {
                "summary": "Плохой Пример",
                "description": "Пример того, как не надо инпутить данные",
                "value": {"title": "Отель_х", "location": ""}
            },
            "2": {
                "summary": "Хороший пример",
                "description": "Пример того, как надо инпутить данные",
                "value": {"title": "Отель_у", "location": "Отличный отель"}
            },
        }
    }