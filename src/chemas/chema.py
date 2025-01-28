from pydantic import BaseModel, Field

class hotel(BaseModel):
    title: str
    rate: str

class hotelPatch(BaseModel):
    title: str | None = Field(None)
    rate: str | None = Field(None)

class Config:
    schema_extra = {
        "examples": {
            "1": {
                "summary": "Плохой Пример",
                "description": "Пример того, как не надо инпутить данные",
                "value": {"title": "Отель_х", "rate": ""}
            },
            "2": {
                "summary": "Хороший пример",
                "description": "Пример того, как надо инпутить данные",
                "value": {"title": "Отель_у", "rate": "Отличный отель"}
            },
        }
    }