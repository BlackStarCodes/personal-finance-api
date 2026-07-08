from pydantic import BaseModel


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

    