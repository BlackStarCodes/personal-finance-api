import pytest
from fastapi import HTTPException
import source.services.transaction_service as ts
from source.enums import WalletGroup, CategoryType


HAVE_BALANCE = [
    (999, WalletGroup.AVAILABLE, CategoryType.EXPENSE),
    (1000, WalletGroup.UNASSIGNED, CategoryType.INVESTMENT),
    (800, WalletGroup.AVAILABLE, CategoryType.SAVINGS),
    (800, WalletGroup.SAVINGS, CategoryType.SAVINGS),
    (900, WalletGroup.AVAILABLE, CategoryType.DEBT),
    (500, WalletGroup.INVESTMENT, CategoryType.EMERGENCY_FUND),
    (1000, WalletGroup.AVAILABLE, CategoryType.EXPENSE),
]

@pytest.mark.parametrize("amt, from_wallet_group, category_type", HAVE_BALANCE)
def test_check_sufficient_balance_accepts_valid_amount(
    amt,
    from_wallet_group,
    category_type,
    wallet_factory,
    category_factory
):  
    from_wallet = wallet_factory(from_wallet_group)
    category = category_factory(category_type)
    ts.check_sufficient_balance(amt, from_wallet, category)


INSUFFICIENT_BALANCE = [
    (1010, WalletGroup.AVAILABLE, CategoryType.EXPENSE),
    (2000, WalletGroup.UNASSIGNED, CategoryType.INVESTMENT),
    (8000, WalletGroup.AVAILABLE, CategoryType.SAVINGS),
    (8000, WalletGroup.SAVINGS, CategoryType.SAVINGS),
    (10000, WalletGroup.AVAILABLE, CategoryType.INVESTMENT),
    (11000, WalletGroup.INVESTMENT, CategoryType.EMERGENCY_FUND),
    (1001, WalletGroup.AVAILABLE, CategoryType.EXPENSE),
]

@pytest.mark.parametrize("amt, from_wallet_group, category_type", INSUFFICIENT_BALANCE)
def test_check_sufficient_balance_rejects_low_balance(
    amt,
    from_wallet_group,
    category_type,
    wallet_factory,
    category_factory
):  
    from_wallet = wallet_factory(from_wallet_group)
    category = category_factory(category_type)

    with pytest.raises(HTTPException) as exc:
        ts.check_sufficient_balance(amt, from_wallet, category)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Insufficient Wallet Balance!"



INCOME = [
    (1010,  CategoryType.INCOME),
    (2000,  CategoryType.INCOME),
    (8000, CategoryType.INCOME),
]

@pytest.mark.parametrize("amt, category_type", INCOME)
def test_check_sufficient_balance_accepts_income(
    amt,
    category_type,
    category_factory
):  
    
    category = category_factory(category_type)

    ts.check_sufficient_balance(amt, from_wallet = None, category = category)



INVALID_AMOUNT = [
    (-1010, WalletGroup.AVAILABLE, CategoryType.EXPENSE),
    (00, WalletGroup.UNASSIGNED, CategoryType.INVESTMENT),
    (-8000.654, WalletGroup.AVAILABLE, CategoryType.SAVINGS),
    (-2, WalletGroup.SAVINGS, CategoryType.SAVINGS),
    (-0.2, WalletGroup.INVESTMENT, CategoryType.INVESTMENT),
    ]

@pytest.mark.parametrize("amt, from_wallet_group, category_type", INVALID_AMOUNT)
def test_check_sufficient_balance_rejects_invalid_amount(
    amt,
    from_wallet_group,
    category_type,
    category_factory,
    wallet_factory
):
    category = category_factory(category_type)
    from_wallet = wallet_factory(from_wallet_group)

    with pytest.raises(HTTPException) as exc:
        ts.check_sufficient_balance(amt, from_wallet, category)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Amount must be above 0!"



DEBT_BYPASS = [
    (1010, WalletGroup.DEBT, CategoryType.EXPENSE),
    (3000, WalletGroup.DEBT, CategoryType.EXPENSE),
    (8000.654, WalletGroup.DEBT, CategoryType.DEBT),
    (2002, WalletGroup.DEBT, CategoryType.DEBT),
    (340.2, WalletGroup.DEBT, CategoryType.DEBT),
    ]

@pytest.mark.parametrize("amt, from_wallet_group, category_type", DEBT_BYPASS)
def test_check_sufficient_balance_accepts_debt(
    amt,
    from_wallet_group,
    category_type,
    category_factory,
    wallet_factory
):
    category = category_factory(category_type)
    from_wallet = wallet_factory(from_wallet_group)

    
    ts.check_sufficient_balance(amt, from_wallet, category)

