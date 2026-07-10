from pydantic import BaseModel, Field
from .enums import WalletType, CategoryType, TransactionMedium, TransactionStatus
from decimal import Decimal
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    fullname: str | None = None
    email: str


class UserRegister(UserCreate):
    password: str


class UserOut(UserCreate):
    id: int
    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class UserUpdate(UserCreate):
    password: str

    
class UserDelete(BaseModel):
    password: str
    confirm: str


class WalletCreate(BaseModel):
    name: str
    type: WalletType
    currency: str = Field(min_length=3, max_length=3)
    balance: Decimal


class WalletOut(WalletCreate):
    id: int
    model_config = {"from_attributes": True}


class WalletUpdate(WalletCreate):
    pass


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType


class CategoryOut(CategoryCreate):
    id: int
    model_config = {"from_attributes":True}


class CategoryUpdate(CategoryCreate):
    pass
    

class TransactionCreate(BaseModel):
    name: str
    from_wallet_id: int
    to_wallet_id: int | None = None
    category_id: int

    amount: Decimal
    transaction_date: datetime
    description: str | None = None
    merchant: str | None = None

    transaction_medium: TransactionMedium
    status: TransactionStatus = TransactionStatus.COMPLETED
    is_recurring: bool = False
    receipt_url: str | None = None
    