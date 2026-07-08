from fastapi import APIRouter, HTTPException, Depends
from ..schemas import UserRegister, UserOut, UserCreate
from ..models.user import UserOrm
from ..dependencies import session_dependency
from ..security import pwd_hashed, get_current_user
from sqlalchemy import select
from typing import Annotated    


router = APIRouter()


@router.post('/', response_model= UserOut)
async def create_user(user:UserRegister, session: session_dependency):
    if session.scalar(select(UserOrm).where(UserOrm.username == user.username)):
        raise HTTPException(status_code=409, detail="Username taken!")
    if session.scalar(select(UserOrm).where(UserOrm.email == user.email)):
        raise HTTPException(status_code=409, detail="Email already in use!")
    new_user = UserOrm(
        username = user.username,
        fullname = user.fullname,
        email = user.email,
        hashed_password = pwd_hashed(user.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get('/me', response_model=UserOut)
async def read_current_user(user: Annotated[UserOrm, Depends(get_current_user)]):
    return user