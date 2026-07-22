import pytest
import source.services.transaction_service as ts
from source.enums import WalletGroup, CategoryType


TWO_WALLET_CASE = [
    (1000, WalletGroup.INVESTMENT, WalletGroup.INVESTMENT, CategoryType.TRANSFER, 2000, 0),
    (100, WalletGroup.INVESTMENT, WalletGroup.SAVINGS, CategoryType.SAVINGS, 1100, 900),
    (2533, WalletGroup.DEBT, WalletGroup.SAVINGS, CategoryType.DEBT, 3533, -1533),
    (734, WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED, CategoryType.TRANSFER, 1734, 266),
    (687, WalletGroup.AVAILABLE, WalletGroup.EMERGENCY_FUND, CategoryType.EMERGENCY_FUND, 1687, 313),
    (45, WalletGroup.DEBT, WalletGroup.AVAILABLE, CategoryType.DEBT, 1045, 955),
    (165, WalletGroup.UNASSIGNED, WalletGroup.INVESTMENT, CategoryType.INVESTMENT, 1165, 835),
    (899, WalletGroup.SAVINGS, WalletGroup.EMERGENCY_FUND, CategoryType.EMERGENCY_FUND, 1899, 101),
]

@pytest.mark.parametrize("amt, from_wallet_grp, to_wallet_grp, category_type, from_bal, to_bal", TWO_WALLET_CASE)
def test_reverse_balance_changes_two_wallet_transactions(
    amt,
    from_wallet_grp,
    to_wallet_grp,
    category_type,
    to_bal,
    from_bal,
    wallet_factory,
    category_factory
):
    
    from_wallet = wallet_factory(from_wallet_grp)
    to_wallet = wallet_factory(to_wallet_grp)
    category = category_factory(category_type)

    ts.reverse_balance_changes(amt, from_wallet, to_wallet, category)

    assert from_wallet.balance == from_bal
    assert to_wallet.balance == to_bal


INCOME_CASE = [
    (200, WalletGroup.AVAILABLE, CategoryType.INCOME, 800),
    (569, WalletGroup.AVAILABLE, CategoryType.INCOME, 431),
    (1000, WalletGroup.UNASSIGNED, CategoryType.INCOME, 0),
]

@pytest.mark.parametrize("amt, to_wallet_grp, category_type, to_bal", INCOME_CASE)
def test_reverse_balance_changes_income_transaction(
    amt,
    to_wallet_grp,
    category_type,
    to_bal,
    wallet_factory,
    category_factory
):
    
    from_wallet = None
    to_wallet = wallet_factory(to_wallet_grp)
    category = category_factory(category_type)

    ts.reverse_balance_changes(amt, from_wallet, to_wallet, category)

    assert to_wallet.balance == to_bal



EXPENSE_CASE = [
    (200, WalletGroup.AVAILABLE, CategoryType.EXPENSE, 1200),
    (43000, WalletGroup.DEBT, CategoryType.EXPENSE, 44000),
    (1000, WalletGroup.UNASSIGNED, CategoryType.EXPENSE, 2000),
    (89500, WalletGroup.DEBT, CategoryType.EXPENSE, 90500),
]

@pytest.mark.parametrize("amt, from_wallet_grp, category_type, from_bal", EXPENSE_CASE)
def test_reverse_balance_changes_expense_transaction(
    amt,
    from_wallet_grp,
    category_type,
    from_bal,
    wallet_factory,
    category_factory
):
    
    to_wallet = None
    from_wallet = wallet_factory(from_wallet_grp)
    category = category_factory(category_type)

    ts.reverse_balance_changes(amt, from_wallet, to_wallet, category)

    assert from_wallet.balance == from_bal

