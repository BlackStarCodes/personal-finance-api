from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func, DateTime, ForeignKey, UniqueConstraint
from ..database import Base
from datetime import datetime


class WalletOrm(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('registered_users.id'))
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(30))
    currency: Mapped[str] = mapped_column(String(3))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("user_id", "name", name="uniq_wallet_name_per_user",))