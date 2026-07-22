import pytest
import source.services.transaction_service as ts
from source.enums import WalletGroup, CategoryType


TWO_WALLET_CASE = [
    (1000, WalletGroup.INVESTMENT, WalletGroup.INVESTMENT, CategoryType.TRANSFER, 0, 2000),
    (100, WalletGroup.INVESTMENT, WalletGroup.SAVINGS, CategoryType.SAVINGS, 900, 1100),
    (2533, WalletGroup.DEBT, WalletGroup.SAVINGS, CategoryType.DEBT, -1533, 3533),
    (734, WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED, CategoryType.TRANSFER, 266, 1734),
    (687, WalletGroup.AVAILABLE, WalletGroup.EMERGENCY_FUND, CategoryType.EMERGENCY_FUND, 313, 1687),
    (45, WalletGroup.DEBT, WalletGroup.AVAILABLE, CategoryType.DEBT, 955, 1045),
    (165, WalletGroup.UNASSIGNED, WalletGroup.INVESTMENT, CategoryType.INVESTMENT, 835, 1165),
    (899, WalletGroup.SAVINGS, WalletGroup.EMERGENCY_FUND, CategoryType.EMERGENCY_FUND, 101, 1899),
]

@pytest.mark.parametrize("amt, from_wallet_grp, to_wallet_grp, category_type, from_bal, to_bal", TWO_WALLET_CASE)
def test_apply_balance_changes_two_wallet_transactions(
    amt,
    from_wallet_grp,
    to_wallet_grp,
    category_type,
    from_bal,
    to_bal,
    wallet_factory,
    category_factory
):
    
    from_wallet = wallet_factory(from_wallet_grp)
    to_wallet = wallet_factory(to_wallet_grp)
    category = category_factory(category_type)

    ts.apply_balance_changes(amt, from_wallet, to_wallet, category)

    assert from_wallet.balance == from_bal
    assert to_wallet.balance == to_bal


INCOME_CASE = [
    (20000, WalletGroup.AVAILABLE, CategoryType.INCOME, 21000),
    (43000, WalletGroup.AVAILABLE, CategoryType.INCOME, 44000),
    (89500, WalletGroup.UNASSIGNED, CategoryType.INCOME, 90500),
]

@pytest.mark.parametrize("amt, to_wallet_grp, category_type, to_bal", INCOME_CASE)
def test_apply_balance_changes_income_transaction(
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

    ts.apply_balance_changes(amt, from_wallet, to_wallet, category)

    assert to_wallet.balance == to_bal



EXPENSE_CASE = [
    (200, WalletGroup.AVAILABLE, CategoryType.EXPENSE, 800),
    (43000, WalletGroup.DEBT, CategoryType.EXPENSE, -42000),
    (1000, WalletGroup.UNASSIGNED, CategoryType.EXPENSE, 0),
    (89500, WalletGroup.DEBT, CategoryType.EXPENSE, -88500),
]

@pytest.mark.parametrize("amt, from_wallet_grp, category_type, from_bal", EXPENSE_CASE)
def test_apply_balance_changes_expense_transaction(
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

    ts.apply_balance_changes(amt, from_wallet, to_wallet, category)

    assert from_wallet.balance == from_bal

