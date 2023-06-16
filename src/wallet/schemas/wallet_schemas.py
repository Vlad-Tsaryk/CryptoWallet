from pydantic import BaseModel, Field

from src.wallet.schemas.currency_schemas import CurrencyResponse


class WalletBase(BaseModel):
    user_id: int
    address: str = Field(max_length=42)


class WalletCreate(WalletBase):
    ...


class WalletAddress(BaseModel):
    address: str = Field(max_length=42)


class WalletPrivateKey(BaseModel):
    private_key: str = Field(max_length=64)


class WalletResponse(WalletBase):
    id: int
    currency: CurrencyResponse
    balance: int

    @property
    def balance(self):
        return 4

    class Config:
        orm_mode = True
