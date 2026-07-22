import pytest
from fastapi import HTTPException
import source.services.transaction_service as ts
from source.enums import WalletGroup


def test_expense_cannot_have_destination_wallet(wallet_factory):
    available_wallet = wallet_factory(WalletGroup.AVAILABLE)    
    with pytest.raises(HTTPException) as exc:
        ts.validate_expense(from_wallet=available_wallet, to_wallet=available_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Expense transaction cannot have a destination wallet!"
    


def test_expense_requires_source_wallet(wallet_factory):
    available_wallet = wallet_factory(WalletGroup.AVAILABLE)

    with pytest.raises(HTTPException) as exc:
        ts.validate_expense(from_wallet=None, to_wallet=available_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Expense transaction needs a source wallet!"



VALID_WALLET_GROUPS = [
        WalletGroup.AVAILABLE,
        WalletGroup.UNASSIGNED,
        WalletGroup.DEBT,
        ]

@pytest.mark.parametrize("from_wallet_group", VALID_WALLET_GROUPS)
def test_expense_accepts_valid_wallet_groups(from_wallet_group, wallet_factory):
     
    from_wallet = wallet_factory(from_wallet_group)

    ts.validate_expense(from_wallet, to_wallet=None)



INVALID_WALLET_GROUPS = [
        WalletGroup.SAVINGS,
        WalletGroup.EMERGENCY_FUND,
        WalletGroup.INVESTMENT,
        ]

@pytest.mark.parametrize("from_wallet_group", INVALID_WALLET_GROUPS)
def test_expense_rejects_invalid_wallet_groups(from_wallet_group, wallet_factory):
     
    from_wallet = wallet_factory(from_wallet_group)

    with pytest.raises(HTTPException) as exc:
        ts.validate_expense(from_wallet, to_wallet=None)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Can only spend from available, unassigned, debt wallets!"