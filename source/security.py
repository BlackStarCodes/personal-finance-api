import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from .dependencies import session_dependency, oauth2_scheme
from .models.user import UserOrm
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from .config import SECRET_KEY, ALGO
from typing import Annotated
from fastapi import HTTPException, status, Depends
from .schemas import TokenData


hasher = PasswordHash.recommended()


def pwd_hashed(pwd) -> str:
    return hasher.hash(pwd)


def verify_pwd(pwd, hashed_pwd) -> bool:
    return hasher.verify(pwd, hashed_pwd)


mock = hasher.hash("Some Pass")


def authenticate_user(
        session: session_dependency, 
        username: str, 
        password: str,
        ) -> UserOrm | bool:
    user = session.scalar(select(UserOrm).where(UserOrm.username == username, UserOrm.deleted_at.is_(None)))
    if not user:
        verify_pwd(password, mock)
        return False
    
    if not verify_pwd(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: session_dependency):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate Credentials!", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        sub = payload.get("sub")
        if not sub:
            raise credentials_exception
        user_id = int(sub)
        if not user_id:
            raise credentials_exception
        token_data = TokenData(id= user_id)
    except InvalidTokenError:
        raise credentials_exception
    user = session.scalar(select(UserOrm).where(UserOrm.id == token_data.id, UserOrm.deleted_at.is_(None)))
    if not user:
        raise credentials_exception
    return user