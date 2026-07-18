import pytest
from fastapi import HTTPException
import source.services.transaction_service as ts
from source.enums import WalletGroup


def test_income_source_cannot_have_source_wallet(wallet_factory):
    available_wallet = wallet_factory(WalletGroup.AVAILABLE)  

    with pytest.raises(HTTPException) as exc:
        ts.validate_income(from_wallet=available_wallet, to_wallet=available_wallet)

    assert exc.value.status_code ==  400
    assert exc.value.detail == "Income transaction cannot have a source wallet!"


def test_income_requires_destination_wallet():

    with pytest.raises(HTTPException) as exc:
        ts.validate_income(from_wallet=None, to_wallet=None)
    
    assert exc.value.status_code == 400
    assert exc.value.detail == "Income transaction needs a destination wallet!"



VALID_WALLET_GROUPS = [
        WalletGroup.AVAILABLE,
        WalletGroup.UNASSIGNED,
        ]

@pytest.mark.parametrize("to_wallet_group", VALID_WALLET_GROUPS)
def test_income_accepts_valid_wallet_groups(to_wallet_group, wallet_factory):
     
    to_wallet = wallet_factory(to_wallet_group)

    ts.validate_income(from_wallet=None, to_wallet = to_wallet)



INVALID_WALLET_GROUPS = [
        WalletGroup.DEBT,
        WalletGroup.SAVINGS,
        WalletGroup.EMERGENCY_FUND,
        WalletGroup.INVESTMENT,
        ]

@pytest.mark.parametrize("to_wallet_group", INVALID_WALLET_GROUPS)
def test_income_rejects_invalid_wallet_groups(to_wallet_group, wallet_factory):
     
    to_wallet = wallet_factory(to_wallet_group)

    with pytest.raises(HTTPException) as exc:
        ts.validate_income(from_wallet=None, to_wallet = to_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Income transaction can only go to Available or Unassigned Wallets!"
