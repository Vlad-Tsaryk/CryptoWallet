from passlib.context import CryptContext
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_file import ImageField

from config.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), index=True)
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    profile_image: Mapped[ImageField] = mapped_column(ImageField, nullable=True)
    _password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    # wallets = relationship("wallet", lazy="dynamic")  # lazy-loading relationship
    # wallets: Mapped[List["Wallet"]] = relationship(
    #     back_populates="user", cascade="all, delete-orphan"
    # )

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext: str):
        if plaintext:
            self._password = pwd_context.hash(plaintext)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)

    # user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    # currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"))
    # balance = Column(Integer, nullable=False)
