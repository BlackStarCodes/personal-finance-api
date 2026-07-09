from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime
from ..database import Base
from datetime import datetime



class UserOrm(Base):
    __tablename__ = 'registered_users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str | None]
    email: Mapped[str] = mapped_column(String(60), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default= func.now(), onupdate=func.now())
    wallets: Mapped[list["WalletOrm"]] = relationship(back_populates="user")
    categories: Mapped[list["CategoryOrm"]] = relationship(back_populates="user")
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )