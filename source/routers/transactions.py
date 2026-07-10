from fastapi import APIRouter, HTTPException
from ..models.transaction import TransactionOrm
from ..dependencies import session_dependency
from sqlalchemy import select, func, exists, or_
from ..schemas import TransactionCreate, TransactionOut, TransactionUpdate