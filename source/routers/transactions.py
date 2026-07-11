from fastapi import APIRouter, HTTPException
from ..models.transaction import TransactionOrm
from ..models.category import CategoryOrm
from ..models.wallet import WalletOrm
from ..dependencies import session_dependency
from sqlalchemy import select, func, exists, or_
from ..schemas import TransactionCreate, TransactionOut, TransactionUpdate
from ..security import current_user
from ..services.transaction_service import validate_wallets, validate_category, validate_category_types,check_sufficient_balance, apply_balance_changes, reverse_balance_changes


router = APIRouter()


@router.post('/', response_model=TransactionOut)
async def create_transaction(   
    user: current_user,
    session: session_dependency,
    transaction: TransactionCreate,
):
    to_wallet, from_wallet = validate_wallets(user_id=user.id, to_wallet_id=transaction.to_wallet_id, from_wallet_id=transaction.from_wallet_id, session=session)
    category = validate_category(user.id, transaction.category_id, session)
    validate_category_types(from_wallet=from_wallet, to_wallet=to_wallet, category=category)
    check_sufficient_balance(transaction.amount, from_wallet, category)
    apply_balance_changes(transaction.amount, from_wallet, to_wallet, category)
    
    new_transaction = TransactionOrm(
        name = transaction.name,
        from_wallet_id= transaction.from_wallet_id,
        to_wallet_id= transaction.to_wallet_id,
        category_id= transaction.category_id,

        amount= transaction.amount,
        transaction_date = transaction.transaction_date,
        description = transaction.description,
        merchant = transaction.merchant,

        transaction_medium = transaction.transaction_medium,
        status = transaction.status,
        is_recurring = transaction.is_recurring,
        receipt_url = transaction.receipt_url,
        )
    

    try: 
        session.add(new_transaction)
        session.commit()
        session.refresh(new_transaction)
    except Exception:
        session.rollback()
        raise

    return new_transaction
    