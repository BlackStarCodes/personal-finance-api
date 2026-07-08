from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime, ForeignKey, UniqueConstraint, Boolean, Enum, text
from ..database import Base
from ..enums import CategoryType
from datetime import datetime


class CategoryOrm(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('registered_users.id'))
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[CategoryType] = mapped_column(Enum(CategoryType))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
        )
    is_default: Mapped[bool] = mapped_column(Boolean, server_default= text("false"))
    user: Mapped["UserOrm"] = relationship(back_populates="categories")
    transactions: Mapped[list["TransactionOrm"]] = relationship(back_populates="category")
    
    __table_args__ = (
        UniqueConstraint(
        "user_id", 
        "name", 
        name="uniq_category_per_user",)
        ,)