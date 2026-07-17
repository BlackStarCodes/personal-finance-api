from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from source.database import get_session


session_dependency = Annotated[Session, Depends(get_session)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

