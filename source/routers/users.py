from fastapi import APIRouter, HTTPException, Depends
from source.schemas import UserRegister, UserOut, UserUpdate, UserDelete
from source.models.user import UserOrm
from source.dependencies import session_dependency
from source.security import pwd_hashed, get_current_user, verify_pwd, current_user
from sqlalchemy import select, func
from datetime import datetime, timezone
from source.services.category_service import seed_default_categories
from source.services.wallet_service import seed_default_wallets


router = APIRouter()


@router.post('/', response_model= UserOut)
async def create_user(user:UserRegister, session: session_dependency):
    user.username = user.username.strip()
    user.email = user.email.strip().lower()
    try:
        if session.scalar(select(UserOrm).where(
            func.lower(UserOrm.username) == user.username.lower())):
            raise HTTPException(status_code=409, detail="Username taken!")
        
        if session.scalar(select(UserOrm).where(
            func.lower(UserOrm.email) == user.email)):
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

        seed_default_categories(new_user.id, session)
        seed_default_wallets(new_user.id, session)
        
        session.commit()
    except Exception:
        session.rollback()
        raise

    return new_user


@router.get('/me', response_model=UserOut)
async def read_current_user(user: current_user):
    return user


@router.put('/me', response_model=UserOut)
async def update_user(
    updated_user: UserUpdate,
    user: current_user,
    session: session_dependency):
    try:
        updated_username = updated_user.username.strip()
        updated_email = updated_user.email.strip().lower()
        
        existing = session.scalar(select(UserOrm).where(
            func.lower(UserOrm.username) == updated_username.lower()))
        
        if existing and existing.id != user.id:
            raise HTTPException(status_code=409, detail= "Username taken!")
        
        existing_email = session.scalar(select(UserOrm).where(
            func.lower(UserOrm.email) == updated_email))
        
        if existing_email and existing_email.id != user.id:
            raise HTTPException(status_code=409, detail= "Email already in use!")
        
        user.username = updated_username
        user.email = updated_email
        user.fullname = updated_user.fullname
        user.hashed_password = pwd_hashed(updated_user.password)

        session.commit()
        session.refresh(user)

    except Exception:
        session.rollback()
        raise
    return user


@router.delete('/me')
async def delete_user(
    user: current_user,
    user_confirm: UserDelete,
    session: session_dependency):

    try:
        if not verify_pwd(user_confirm.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Password is incorrect!")
        
        if not user_confirm.confirm == "DELETE MY ACCOUNT":
            raise HTTPException(status_code=400, detail= "Confirm message must be 'DELETE MY ACCOUNT'.")
        user.deleted_at = datetime.now(timezone.utc)
        session.commit()

    except Exception:
        session.rollback()
        raise
    
    return {"message": "Account deleted successfully"}
    

