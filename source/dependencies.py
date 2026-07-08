from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_session


session_dependency = Annotated[Session, Depends(get_session)]