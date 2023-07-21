from datetime import datetime
from typing import List

from sqlalchemy import (
    String,
    ForeignKey,
    UniqueConstraint,
    SmallInteger,
    DateTime,
    Float,
    Integer,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_file import ImageField

from config.database import Base
from src.ibay.models import Product
from src.users.models import User


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(254), index=True)
    decimal_places: Mapped[int] = mapped_column(SmallInteger)
    image: Mapped[ImageField] = mapped_column(ImageField)
    blockchain_id = mapped_column(ForeignKey("blockchain.id"))

    # blockchain: Mapped["Blockchain"] = relationship(back_populates="currencies")
    wallets: Mapped[List["Wallet"]] = relationship(
        back_populates="currency", cascade="all, delete-orphan"
    )


class Wallet(Base):
    __tablename__ = "wallet"
    __table_args__ = (
        UniqueConstraint("address", "currency_id", name="unique_address_currency"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(42))
    private_key: Mapped[str] = mapped_column(String(64))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"))

    owner = relationship(User, back_populates="wallets")
    currency: Mapped["Currency"] = relationship(Currency, back_populates="wallets")
    products: Mapped[List["Product"]] = relationship(
        back_populates="wallet", cascade="all, delete-orphan"
    )
    # currency = relationship("Currency")
    # shipping_address = relationship("Address")

    # wallets = relationship("Wallet")


class Blockchain(Base):
    __tablename__ = "blockchain"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(254), index=True)
    rpc_url: Mapped[str]
    chain_id: Mapped[int]

    # currencies: Mapped[List["Currency"]] = relationship(
    #     back_populates="currency", cascade="all, delete-orphan"
    # )


STATUS_CHOICES: ENUM = ENUM("SUCCESS", "FAILED", "PENDING", name="status_choices")


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    tnx_hash: Mapped[str] = mapped_column(String(66))
    from_address: Mapped[str] = mapped_column(String(42), index=True)
    to_address: Mapped[str] = mapped_column(String(42), index=True)
    value: Mapped[float] = mapped_column(Float)
    age: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    tnx_fee: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(10), STATUS_CHOICES, default="PENDING")


class ParsedBlock(Base):
    __tablename__ = "parsed_block"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(Integer)
