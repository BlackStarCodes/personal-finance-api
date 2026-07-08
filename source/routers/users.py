from fastapi import APIRouter, HTTPException
from ..schemas import UserRegister, UserOut
from ..models.user import UserOrm
from ..dependencies import session_dependency
from ..security import pwd_hashed
from sqlalchemy import select

router = APIRouter()


@router.post('/users', response_model= UserOut)
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