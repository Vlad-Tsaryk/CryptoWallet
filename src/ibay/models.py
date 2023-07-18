from datetime import datetime

from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_file import ImageField

from config.database import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), index=True)
    photo: Mapped[ImageField] = mapped_column(ImageField)
    price: Mapped[float] = mapped_column(Float)
    wallet_id = mapped_column(ForeignKey("wallet.id"))


STATUS_CHOICES: ENUM = ENUM(
    "NEW", "RETURN" "SUCCESS", "FAILED", "DELIVERY", name="status_choices"
)


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    product_id = mapped_column(ForeignKey("product.id"))
    time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    status: Mapped[str] = mapped_column(String(10), STATUS_CHOICES, default="NEW")
    return_address: Mapped[str] = mapped_column(String(42))
