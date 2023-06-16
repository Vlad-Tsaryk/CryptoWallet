from pydantic import BaseModel


class CurrencyResponse(BaseModel):
    name: str
    image: dict | None = None
    decimal_places: int

    class Config:
        orm_mode = True
