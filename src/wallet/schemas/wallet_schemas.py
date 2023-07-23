from pydantic import BaseModel, Field

from src.wallet.schemas.currency_schemas import CurrencyResponse


class WalletBase(BaseModel):
    user_id: int
    address: str = Field(max_length=42, min_length=42)


class WalletCreate(WalletBase):
    private_key: str = Field(max_length=64, min_length=64)


class WalletAddress(BaseModel):
    address: str = Field(max_length=42, min_length=42)


class WalletPrivateKey(BaseModel):
    private_key: str = Field(max_length=64, min_length=64)


class WalletResponse(WalletBase):
    id: int
    currency: CurrencyResponse

    class Config:
        orm_mode = True


class WalletRelationResponse(BaseModel):
    id: int
    address: str

    class Config:
        orm_mode = True
