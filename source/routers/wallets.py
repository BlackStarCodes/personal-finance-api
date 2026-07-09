from fastapi import APIRouter, HTTPException, Query, Depends, status
from ..models.wallet import WalletOrm
from ..models.user import UserOrm   
from ..schemas import WalletCreate, WalletOut, WalletUpdate
from typing import Annotated
from ..dependencies import session_dependency
from ..security import get_current_user
from sqlalchemy import select, func



router = APIRouter()


@router.post('/', response_model= WalletOut)
async def create_wallet(
    user: Annotated[UserOrm, Depends(get_current_user)],
    wallet: WalletCreate,
    session: session_dependency,):
    wallet_name = wallet.name.strip().lower()

    existing_wallet = session.scalar(select(WalletOrm).where(
        WalletOrm.user_id == user.id,
        func.lower(WalletOrm.name) == wallet_name
    ))
    if existing_wallet:
        raise HTTPException(status_code=409, detail="Wallet name already exists!")
    
    new_wallet = WalletOrm(
        user_id = user.id,
        name = wallet_name,
        type = wallet.type,
        currency = wallet.currency,
        balance = wallet.balance
    )
    session.add(new_wallet)
    session.commit()
    session.refresh(new_wallet)
    return new_wallet