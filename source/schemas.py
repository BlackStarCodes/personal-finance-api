from pydantic import BaseModel, Field
from .enums import WalletType
from decimal import Decimal


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