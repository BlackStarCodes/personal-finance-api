from source.models.wallet import WalletOrm
from source.models.category import CategoryOrm
from source.models.transaction import TransactionOrm
from fastapi import HTTPException
from source.enums import CategoryType, WalletGroup
from sqlalchemy import select, or_


# ============================
# Wallet Validation
# ============================


def validate_wallets(user_id, to_wallet_id : int | None, from_wallet_id: int | None, session):
    to_wallet = session.scalar(select(WalletOrm).where(WalletOrm.id == to_wallet_id, WalletOrm.user_id == user_id))
    from_wallet = session.scalar(select(WalletOrm).where(WalletOrm.id == from_wallet_id, WalletOrm.user_id == user_id))

    if from_wallet_id is not None and from_wallet is None:
            raise HTTPException(404,detail= "Source wallet not found.")

    if to_wallet_id is not None and to_wallet is None:
        raise HTTPException(404,detail= "Destination wallet not found.")
    
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
   

# ============================
# Transaction Rule Validation
# ============================


def validate_transaction_rules(category: CategoryType, from_wallet: WalletOrm | None, to_wallet: WalletOrm | None):
    
    validators = {
        CategoryType.INCOME: validate_income,
        CategoryType.EXPENSE: validate_expense,
        CategoryType.SAVINGS: validate_savings,
        CategoryType.EMERGENCY_FUND: validate_emergency_fund,
        CategoryType.INVESTMENT: validate_investment,
        CategoryType.DEBT: validate_debt,
        CategoryType.TRANSFER: validate_transfer,
    }

    validator = validators.get(category.type)

    if validator is None:
        raise HTTPException(400, "Category type not found!")

    validator(from_wallet, to_wallet)



def validate_income(from_wallet: WalletOrm | None, to_wallet: WalletOrm):
    if to_wallet is None:
        raise HTTPException(400, "Income transaction needs a destination wallet!")
    
    if from_wallet:
        raise HTTPException(400, "Income transaction cannot have a source wallet!")

    if to_wallet.wallet_group not in {WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED}:
        raise HTTPException(status_code=400, detail="Income transaction can only go to Available or Unassigned Wallets!")



def validate_expense(from_wallet: WalletOrm | None, to_wallet: WalletOrm | None):
    if from_wallet is None:
        raise HTTPException(400, "Expense transaction needs a source wallet!")
    
    if to_wallet:
        raise HTTPException(400, "Expense transaction cannot have a destination wallet!")

    if from_wallet.wallet_group not in {WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED, WalletGroup.DEBT}:
        raise HTTPException(status_code=400, detail="Can only spend from available, unassigned, debt wallets!")
    


def validate_savings(from_wallet: WalletOrm | None, to_wallet: WalletOrm | None):
    if from_wallet is None:
        raise HTTPException(400, "Savings transaction needs a source wallet!")
    
    if to_wallet is None:
        raise HTTPException(400, "Savings transaction needs a destination wallet!")
    
    if from_wallet.wallet_group == WalletGroup.DEBT or to_wallet.wallet_group == WalletGroup.DEBT:
        raise HTTPException(400, "This is Debt transaction not a Savings transaction")

    if from_wallet.wallet_group == WalletGroup.SAVINGS and to_wallet.wallet_group == WalletGroup.SAVINGS:
        raise HTTPException(status_code=400, detail="Savings to Savings is a Transfer transaction!")
    
    if to_wallet.wallet_group not in {WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED, WalletGroup.SAVINGS} and from_wallet.wallet_group != WalletGroup.SAVINGS:
        raise HTTPException(status_code=400, detail="Invalid Savings transaction!")

    if from_wallet.wallet_group in {WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED} and to_wallet.wallet_group != WalletGroup.SAVINGS:
        raise HTTPException(status_code=400, detail="Invalid Savings transaction!")



def validate_emergency_fund(from_wallet: WalletOrm | None, to_wallet: WalletOrm | None):
    if from_wallet is None:
        raise HTTPException(400, "Emergency Fund transaction needs a source wallet!")
    
    if to_wallet is None:
        raise HTTPException(400, "Emergency Fund transaction needs a destination wallet!")

    if from_wallet.wallet_group == WalletGroup.DEBT or to_wallet.wallet_group == WalletGroup.DEBT:
        raise HTTPException(400, "This is Debt transaction not an Emergency Fund transaction")
   
    if from_wallet.wallet_group == WalletGroup.EMERGENCY_FUND and to_wallet.wallet_group == WalletGroup.EMERGENCY_FUND:
        raise HTTPException(status_code=400, detail="Emergency Fund to Emergency Fund is a Transfer transaction!")
    
    if to_wallet.wallet_group not in {WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED, WalletGroup.EMERGENCY_FUND} and from_wallet.wallet_group != WalletGroup.EMERGENCY_FUND:
        raise HTTPException(status_code=400, detail="Invalid Emergency Fund Transaction!") 

    if from_wallet.wallet_group in {WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED} and to_wallet.wallet_group != WalletGroup.EMERGENCY_FUND:
        raise HTTPException(status_code=400, detail="Invalid Emergency Fund transaction!")



def validate_investment(from_wallet: WalletOrm | None, to_wallet: WalletOrm | None):
    if from_wallet is None:
        raise HTTPException(400, "Investment transaction needs a source wallet!")
    
    if to_wallet is None:
        raise HTTPException(400, "Investment transaction needs a destination wallet!")

    if from_wallet.wallet_group == WalletGroup.DEBT or to_wallet.wallet_group == WalletGroup.DEBT:
        raise HTTPException(400, "This is Debt transaction not an Investment transaction")

    if to_wallet.wallet_group not in {WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED, WalletGroup.INVESTMENT} and from_wallet.wallet_group != WalletGroup.INVESTMENT:
        raise HTTPException(status_code=400, detail="Invalid Investment Transaction!") 

    if from_wallet.wallet_group in {WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED} and to_wallet.wallet_group != WalletGroup.INVESTMENT:
        raise HTTPException(status_code=400, detail="Invalid Investment transaction!")



def validate_transfer(from_wallet: WalletOrm | None, to_wallet: WalletOrm | None):
    
    if from_wallet.wallet_group in {WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED} and to_wallet.wallet_group in {WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED}:
        pass

    elif from_wallet.wallet_group == WalletGroup.EMERGENCY_FUND and to_wallet.wallet_group == WalletGroup.EMERGENCY_FUND:
        pass 
    
    elif from_wallet.wallet_group == WalletGroup.SAVINGS and to_wallet.wallet_group == WalletGroup.SAVINGS:
        pass

    else:
        raise HTTPException(400, "Invalid Transfer Transaction!")



def validate_debt(from_wallet: WalletOrm | None, to_wallet:  WalletOrm | None):
    if from_wallet is None:
        raise HTTPException(400, "Debt transaction needs a source wallet!")
    
    if to_wallet is None:
        raise HTTPException(400, "Debt transaction needs a destination wallet!")

    if to_wallet.wallet_group not in {WalletGroup.DEBT} and from_wallet.wallet_group not in {WalletGroup.DEBT}:
        raise HTTPException(status_code=400, detail="Invalid Debt Transaction!")


# ============================
# Balance Operations
# ============================


def check_sufficient_balance(amount, from_wallet: WalletOrm | None, category):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be above 0!")

    
    if category.type != CategoryType.INCOME and from_wallet.wallet_group != WalletGroup.DEBT:
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
    


def reverse_balance_changes(amount, from_wallet: WalletOrm | None, to_wallet: WalletOrm | None, category):
    if category.type == CategoryType.INCOME:
        to_wallet.balance -= amount
        
        
    elif category.type == CategoryType.EXPENSE:
        from_wallet.balance += amount
        

    else:
        from_wallet.balance += amount
        to_wallet.balance -= amount


# ============================
# Database Helpers
# ============================


def get_user_transaction(transaction_id, user_id, session):
    transaction = session.scalar(select(TransactionOrm).where(TransactionOrm.id == transaction_id
                    , or_(TransactionOrm.from_wallet.has(WalletOrm.user_id == user_id),
                          TransactionOrm.to_wallet.has(WalletOrm.user_id == user_id)
                          )
                          ))
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction Not Found!")
    
    return transaction
    