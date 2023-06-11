from sqlalchemy import String, ForeignKey, UniqueConstraint, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class Wallet(Base):
    __tablename__ = "wallet"
    __table_args__ = (
        UniqueConstraint("address", "currency_id", name="unique_address_currency"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(42))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"))

    owner = relationship("User", back_populates="wallets")
    # currency: Mapped["Currency"] = relationship(back_populates="wallets")


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(254), index=True)
    decimal_places: Mapped[int] = mapped_column(SmallInteger)
    image: Mapped[str] = mapped_column(String(100), unique=True)
    blockchain_id = mapped_column(ForeignKey("blockchain.id"))

    # blockchain: Mapped["Blockchain"] = relationship(back_populates="currencies")
    # wallets: Mapped[List["Wallet"]] = relationship(
    #     back_populates="wallet", cascade="all, delete-orphan"
    # )


class Blockchain(Base):
    __tablename__ = "blockchain"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(254), index=True)
    rpc_url: Mapped[str]
    chain_id: Mapped[int]

    # currencies: Mapped[List["Currency"]] = relationship(
    #     back_populates="currency", cascade="all, delete-orphan"
    # )
