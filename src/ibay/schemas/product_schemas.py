from fastapi import UploadFile
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    title: str = Field(max_length=50)
    wallet_id: int
    price: float = Field(gt=0)
    photo: dict


class ProductCreate(ProductBase):
    photo: UploadFile


class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
