from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func, DateTime, ForeignKey, UniqueConstraint
from ..database import Base
from datetime import datetime


class TransactionOrm(Base):
    __tablename__ = "transactions"

    