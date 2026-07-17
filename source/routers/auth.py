from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from source.config import TOKEN_EXPIRE_MINS
from source.security import create_access_token, authenticate_user
from datetime import timedelta
from typing import Annotated
from source.schemas import Token
from source.dependencies import session_dependency


router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: session_dependency):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password!", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINS)
    access_token = create_access_token(data={"sub":str(user.id)}, expire_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")