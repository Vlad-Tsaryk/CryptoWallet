from pydantic import BaseModel, Field


class WalletBase(BaseModel):
    user_id: int
    address: str = Field(max_length=42)


class WalletCreate(WalletBase):
    ...


class WalletAddress(BaseModel):
    address: str = Field(max_length=42)


class WalletPrivateKey(BaseModel):
    private_key: str = Field(max_length=64)


class CurrencyResponse(BaseModel):
    name: str
    image: str
    decimal_places: int

    class Config:
        orm_mode = True


class WalletResponse(WalletBase):
    id: int
    currency: CurrencyResponse
    balance: int

    @property
    def balance(self):
        return 4

    class Config:
        orm_mode = True
