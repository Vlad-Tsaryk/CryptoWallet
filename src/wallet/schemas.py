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


class WalletResponse(WalletBase):
    class Config:
        orm_mode = True
