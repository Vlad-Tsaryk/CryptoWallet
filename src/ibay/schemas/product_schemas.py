from fastapi import UploadFile
from pydantic import BaseModel, Field

from src.wallet.schemas.wallet_schemas import WalletRelationResponse


class ProductBase(BaseModel):
    title: str = Field(max_length=50)
    wallet_id: int
    price: float = Field(gt=0)
    photo: dict


class ProductCreate(ProductBase):
    photo: UploadFile


class ProductResponse(ProductBase):
    id: int
    wallet: WalletRelationResponse

    class Config:
        orm_mode = True
