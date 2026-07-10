from ..models.wallet import WalletOrm
from ..models.category import CategoryOrm
from fastapi import HTTPException
from ..enums import CategoryType


def validate_wallets(user_id, to_wallet_id : int | None, from_wallet_id: int | None, session):
    to_wallet = session.scalar(select(WalletOrm).where(WalletOrm.id == to_wallet_id, WalletOrm.user_id == user_id))
    from_wallet = session.scalar(select(WalletOrm).where(WalletOrm.id == from_wallet_id, WalletOrm.user_id == user_id))

    if (
    to_wallet_id is not None
    and from_wallet_id is not None
    and to_wallet_id == from_wallet_id
    ):
        raise HTTPException(status_code=400, detail='Source and destination wallet cannot be the same!')
    
    return to_wallet, from_wallet
    


def validate_category(user_id, category_id, session):
    category = session.scalar(select(CategoryOrm).where(CategoryOrm.id == category_id, CategoryOrm.user_id == user_id))
    if not category:
        raise HTTPException(status_code=404, detail="Category Not Found!")
    return category



def validate_category_types(from_wallet: WalletOrm | None, to_wallet: WalletOrm | None, category):
    
    if category.type == CategoryType.INCOME:
        if not to_wallet:
            raise HTTPException(status_code=400, detail="Invalid wallet combination!")
        
    elif category.type == CategoryType.EXPENSE:
        if not from_wallet:
            raise HTTPException(status_code=400, detail="Invalid wallet combination!")

    else:
        if not (to_wallet and from_wallet):
            raise HTTPException(status_code=400, detail="Invalid wallet combination!")
    


def check_sufficient_balance(amount, from_wallet: WalletOrm | None, category):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be above 0!")

    
    if category.type != CategoryType.INCOME:
        if from_wallet.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient Wallet Balance!")

    return True
    


def apply_balance_changes(amount, from_wallet: WalletOrm | None, to_wallet: WalletOrm | None, category):
    if category.type == CategoryType.INCOME:
        to_wallet.balance += amount
        
        
    elif category.type == CategoryType.EXPENSE:
        from_wallet.balance -= amount
        

    else:
        from_wallet.balance -= amount
        to_wallet.balance += amount
    

