import jwt
from pwdlib import PasswordHash
from .dependencies import session_dependency, oauth2_scheme
from .models.user import UserOrm
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from .config import SECRET_KEY, ALGO



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
    user = session.scalar(select(UserOrm).where(UserOrm.username == username))
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
