from pydantic import BaseModel, Field, EmailStr

class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    email: EmailStr


class UserHashedPass(User):
    hashed_password: str

class hotelAdd(BaseModel):
    title: str
    location: str

class hotel(hotelAdd):
    id: int

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