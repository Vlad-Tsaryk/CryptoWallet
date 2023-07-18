from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    success = "SUCCESS"
    failed = "FAILED"
    pending = "PENDING"


class TransactionBase(BaseModel):
    tnx_hash: str = Field(max_length=66)
    from_address: str = Field(max_length=42)
    to_address: str = Field(max_length=42)
    value: float
    tnx_fee: float
    status: StatusEnum = Field(default=StatusEnum.pending)


class TransactionCreate(BaseModel):
    # from_wallet_id: int
    to_address: str = Field(max_length=42)
    value: float = Field(ge=0)


class TransactionCreateOrUpdate(TransactionBase):
    # from_wallet_id: int
    to_address: str = Field(max_length=42)
    value: float = Field(ge=0)
    age: datetime | None
