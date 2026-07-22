from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime, ForeignKey, UniqueConstraint, Boolean, Numeric, Enum
from source.database import Base
from source.enums import TransactionMedium, TransactionStatus
from datetime import datetime
from decimal import Decimal


class TransactionOrm(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    to_wallet_id: Mapped[int | None] = mapped_column(ForeignKey('wallets.id'))
    from_wallet_id: Mapped[int | None] = mapped_column(ForeignKey('wallets.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    amount: Mapped[Decimal] = mapped_column(Numeric(12,2))
    transaction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default= func.now(), onupdate=func.now())    
    description: Mapped[str | None] = mapped_column(String(400))

    merchant: Mapped[str | None] = mapped_column(String(150))
    transaction_medium: Mapped[TransactionMedium] = mapped_column(
        Enum(TransactionMedium,
            values_callable = lambda enum: [e.value for e in enum]))
    
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus,
            values_callable= lambda enum: [e.value for e in enum]), server_default="completed")
    
    
    is_recurring: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)
    receipt_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
        )
    
    category: Mapped["CategoryOrm"] = relationship(back_populates="transactions")

    to_wallet:Mapped['WalletOrm'] = relationship("WalletOrm", foreign_keys=[to_wallet_id], back_populates="incoming_transactions")
    from_wallet:Mapped['WalletOrm'] = relationship("WalletOrm", foreign_keys=[from_wallet_id], back_populates="outgoing_transactions")

