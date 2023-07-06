from enum import Enum

from pydantic import BaseModel, Field


class Status(str, Enum):
    success = "SUCCESS"
    failed = "FAILED"
    pending = "PENDING"


class TransactionBase(BaseModel):
    tnx_hash: str = Field(max_length=64)
    from_address: str = Field(max_length=42)
    to_address: str = Field(max_length=42)
    value: float
    tnx_fee: float
    status: Status = Field(alias="Status")


class TransactionCreate(BaseModel):
    from_wallet_id: int
    to_address: str = Field(max_length=42)
    value: float = Field(ge=0)
