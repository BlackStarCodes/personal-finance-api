from fastapi import APIRouter, HTTPException, Depends
from ..schemas import UserRegister, UserOut, UserUpdate, UserDelete
from ..models.user import UserOrm
from ..dependencies import session_dependency
from ..security import pwd_hashed, get_current_user, verify_pwd
from sqlalchemy import select
from typing import Annotated    
from datetime import datetime, timezone

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


@router.put('/me', response_model=UserOut)
async def update_user(
    updated_user: UserUpdate,
    user: Annotated[UserOrm, Depends(get_current_user)],
    session: session_dependency):
    
    existing = session.scalar(select(UserOrm).where(UserOrm.username == updated_user.username))
    if existing and existing.id != user.id:
        raise HTTPException(status_code=409, detail= "Username taken!")
    
    existing_email = session.scalar(select(UserOrm).where(UserOrm.email == updated_user.email))
    if existing_email and existing_email.id != user.id:
        raise HTTPException(status_code=409, detail= "Email already in use!")
    
    user.username = updated_user.username
    user.email = updated_user.email
    user.fullname = updated_user.fullname
    user.hashed_password = pwd_hashed(updated_user.password)

    session.commit()
    session.refresh(user)
    return user


@router.delete('/me')
async def delete_user(
    user: Annotated[UserOrm, Depends(get_current_user)],
    user_confirm: UserDelete,
    session: session_dependency):
    if not verify_pwd(user_confirm.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Password is incorrect!")
    
    if not user_confirm.confirm == "DELETE MY ACCOUNT":
        raise HTTPException(status_code=400, detail= "Confirm message must be 'DELETE MY ACCOUNT'.")
    user.deleted_at = datetime.now(timezone.utc)
    session.commit()
    return {"message": "Account deleted successfully"}
    

