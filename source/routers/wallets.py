from fastapi import APIRouter, HTTPException, Query, Depends, status
from ..models.wallet import WalletOrm
from ..models.user import UserOrm   
from ..schemas import WalletCreate, WalletOut, WalletUpdate
from typing import Annotated
from ..dependencies import session_dependency
from ..security import get_current_user, current_user
from sqlalchemy import select, func



router = APIRouter()


@router.post('/', response_model= WalletOut)
async def create_wallet(
    user: current_user,
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


@router.get("/", response_model=list[WalletOut])
async def read_wallets(
    user: current_user,
    session: session_dependency,):

    wallets = session.scalars(select(WalletOrm).where(WalletOrm.user_id == user.id)).all()
    return wallets


@router.get("/{wallet_id}", response_model=WalletOut)
async def read_wallet(
    user: current_user,
    wallet_id: int,
    session: session_dependency
):
    wallet = session.scalar(select(WalletOrm).where(WalletOrm.id == wallet_id, WalletOrm.user_id == user.id))
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet Not Found!")
    return wallet


@router.put("/{wallet_id}", response_model=WalletOut)
async def update_wallet(
    wallet_id : int,
    user: current_user,
    wallet: WalletUpdate,
    session: session_dependency
):
    db_wallet = session.scalar(select(WalletOrm).where(WalletOrm.id == wallet_id, WalletOrm.user_id == user.id))
    if not db_wallet:
        raise HTTPException(status_code=401, detail="Not allowed to modify this Wallet!")
    
    wallet_name = wallet.name.strip().lower()
    
    existing_wallet = session.scalar(select(WalletOrm).where(
        WalletOrm.user_id == user.id,
        func.lower(WalletOrm.name) == wallet_name))
    
    if existing_wallet and existing_wallet.id != wallet_id:
        raise HTTPException(status_code=409, detail="Wallet name already exists!")
    

    db_wallet.name = wallet_name
    db_wallet.type = wallet.type
    db_wallet.currency = wallet.currency
    db_wallet.balance = wallet.balance


    session.add(db_wallet)
    session.commit()
    session.refresh(db_wallet)
    return db_wallet
    