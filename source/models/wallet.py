from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime, ForeignKey, UniqueConstraint, Enum, Numeric, text
from ..database import Base
from datetime import datetime
from ..enums import WalletType
from decimal import Decimal


class WalletOrm(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('registered_users.id'))
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[WalletType] = mapped_column(Enum(WalletType,
                                            values_callable = lambda enum: [e.value for e in enum]))
    currency: Mapped[str] = mapped_column(String(3))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default= func.now(), onupdate=func.now())
    user: Mapped["UserOrm"] = relationship(back_populates="wallets")
    balance: Mapped[Decimal] = mapped_column(Numeric(12,2), server_default=text("0"))
    incoming_transactions: Mapped[list["TransactionOrm"]] = relationship(foreign_keys= '[TransactionOrm.to_wallet_id]', back_populates="to_wallet")
    outgoing_transactions: Mapped[list["TransactionOrm"]] = relationship(foreign_keys= '[TransactionOrm.from_wallet_id]', back_populates="from_wallet")

    __table_args__ = (UniqueConstraint("user_id", "name", name="uniq_wallet_name_per_user",),)