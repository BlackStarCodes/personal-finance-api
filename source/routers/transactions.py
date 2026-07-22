from fastapi import APIRouter
from source.models.transaction import TransactionOrm
from source.models.wallet import WalletOrm
from source.dependencies import session_dependency
from sqlalchemy import select, or_
from source.schemas import TransactionCreate, TransactionOut, TransactionUpdate
from source.security import current_user
from source.services.transaction_service import validate_wallets, validate_category, validate_transaction_rules,check_sufficient_balance, apply_balance_changes, reverse_balance_changes, get_user_transaction


router = APIRouter()


@router.post('/', response_model=TransactionOut)
async def create_transaction(   
    user: current_user,
    session: session_dependency,
    transaction: TransactionCreate,
):
    try: 
        to_wallet, from_wallet = validate_wallets(user_id=user.id, to_wallet_id=transaction.to_wallet_id, from_wallet_id=transaction.from_wallet_id, session=session)
        category = validate_category(user.id, transaction.category_id, session)
        
        validate_transaction_rules(from_wallet=from_wallet, to_wallet=to_wallet, category=category)
        check_sufficient_balance(transaction.amount, from_wallet, category)
        apply_balance_changes(transaction.amount, from_wallet, to_wallet, category)
        
        new_transaction = TransactionOrm(
            name = transaction.name.strip() if transaction.name else None,
            from_wallet_id= transaction.from_wallet_id,
            to_wallet_id= transaction.to_wallet_id,
            category_id= transaction.category_id,

            amount= transaction.amount,
            transaction_date = transaction.transaction_date,
            description = transaction.description.strip() if transaction.description else None,
            merchant = transaction.merchant.strip() if transaction.merchant else None,

            transaction_medium = transaction.transaction_medium,
            status = transaction.status,
            is_recurring = transaction.is_recurring,
            receipt_url = transaction.receipt_url.strip() if transaction.receipt_url else None,)
        
    
        session.add(new_transaction)
        session.commit()
        session.refresh(new_transaction)
    
    except Exception:
        session.rollback()
        raise

    return new_transaction
    

@router.get('/', response_model=list[TransactionOut])
async def read_transactions(
    user: current_user,
    session: session_dependency
):
    transactions = session.scalars(select(TransactionOrm).where(or_
        (
        TransactionOrm.from_wallet.has(WalletOrm.user_id == user.id),
        TransactionOrm.to_wallet.has(WalletOrm.user_id == user.id)
        )
        ).order_by(TransactionOrm.transaction_date.desc())
        ).all()

    return transactions


@router.get('/{transaction_id}', response_model=TransactionOut)
async def read_transaction(
    user: current_user,
    session: session_dependency,
    transaction_id: int,
):
    transaction = get_user_transaction(transaction_id=transaction_id, user_id=user.id, session=session)
    
    return transaction 


@router.put('/{transaction_id}', response_model=TransactionOut)
async def update_transaction(
    user: current_user,
    transaction_id: int,
    transaction: TransactionUpdate,
    session: session_dependency
):
    db_transaction = get_user_transaction(transaction_id, user.id, session)

    try: 
        reverse_balance_changes(db_transaction.amount, db_transaction.from_wallet, db_transaction.to_wallet, db_transaction.category)

        to_wallet, from_wallet = validate_wallets(user_id=user.id, to_wallet_id=transaction.to_wallet_id, from_wallet_id=transaction.from_wallet_id, session=session)
        category = validate_category(user.id, transaction.category_id, session)
        validate_transaction_rules(from_wallet=from_wallet, to_wallet=to_wallet, category=category)
        check_sufficient_balance(transaction.amount, from_wallet, category)
        apply_balance_changes(transaction.amount, from_wallet, to_wallet, category)

        db_transaction.name = transaction.name.strip() if transaction.name else None
        db_transaction.from_wallet_id= transaction.from_wallet_id
        db_transaction.to_wallet_id= transaction.to_wallet_id
        db_transaction.category_id= transaction.category_id

        db_transaction.amount= transaction.amount
        db_transaction.transaction_date = transaction.transaction_date
        db_transaction.description = transaction.description.strip() if transaction.description else None
        db_transaction.merchant = transaction.merchant.strip() if transaction.merchant else None

        db_transaction.transaction_medium = transaction.transaction_medium
        db_transaction.status = transaction.status
        db_transaction.is_recurring = transaction.is_recurring
        db_transaction.receipt_url = transaction.receipt_url.strip() if transaction.receipt_url else None
            

        session.commit()
        session.refresh(db_transaction)
    except Exception:
        session.rollback()
        raise

    return db_transaction


@router.delete('/{transaction_id}')
async def delete_transaction(
    user: current_user,
    session: session_dependency,
    transaction_id: int,
):
    try:
        transaction = get_user_transaction(transaction_id, user.id, session)
        reverse_balance_changes(transaction.amount, transaction.from_wallet, transaction.to_wallet, transaction.category)
        
        session.delete(transaction)
        session.commit()

        return {"message": "Successfully deleted transaction!"}
    
    except Exception:
        session.rollback()
        raise
    