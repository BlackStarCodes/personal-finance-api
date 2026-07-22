import pytest
from fastapi import HTTPException
import source.services.transaction_service as ts
from source.enums import WalletGroup


def test_savings_requires_source_wallet(wallet_factory):
    savings_wallet = wallet_factory(WalletGroup.SAVINGS)
    with pytest.raises(HTTPException) as exc:
        ts.validate_savings(from_wallet=None, to_wallet=savings_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Savings transaction needs a source wallet!"


def test_savings_requires_destination_wallet(wallet_factory):
    savings_wallet = wallet_factory(WalletGroup.SAVINGS)
    with pytest.raises(HTTPException) as exc:
        ts.validate_savings(from_wallet=savings_wallet, to_wallet=None)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Savings transaction needs a destination wallet!"


VALID_PAIRS = [
        (WalletGroup.AVAILABLE, WalletGroup.SAVINGS),
        (WalletGroup.UNASSIGNED, WalletGroup.SAVINGS),
        (WalletGroup.SAVINGS, WalletGroup.AVAILABLE),
        (WalletGroup.SAVINGS, WalletGroup.UNASSIGNED),
        (WalletGroup.INVESTMENT, WalletGroup.SAVINGS),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.SAVINGS),]

@pytest.mark.parametrize("from_wallet_group, to_wallet_group", VALID_PAIRS)

def test_savings_accepts_valid_wallet_groups(from_wallet_group, to_wallet_group, wallet_factory):
     
    from_wallet = wallet_factory(from_wallet_group)
    to_wallet = wallet_factory(to_wallet_group)

    ts.validate_savings(from_wallet, to_wallet)



INVALID_PAIRS = [
        (WalletGroup.DEBT, WalletGroup.SAVINGS),
        (WalletGroup.SAVINGS, WalletGroup.DEBT),
        (WalletGroup.SAVINGS, WalletGroup.SAVINGS),
        (WalletGroup.SAVINGS, WalletGroup.INVESTMENT),
        (WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED),
        (WalletGroup.INVESTMENT, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.SAVINGS, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.UNASSIGNED, WalletGroup.UNASSIGNED),
        (WalletGroup.AVAILABLE, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.UNASSIGNED, WalletGroup.DEBT),
        (WalletGroup.INVESTMENT, WalletGroup.AVAILABLE),
        (WalletGroup.DEBT, WalletGroup.INVESTMENT),
        ]


@pytest.mark.parametrize("from_wallet_group, to_wallet_group", INVALID_PAIRS)

def test_savings_rejects_invalid_wallet_groups(from_wallet_group, to_wallet_group, wallet_factory):
     
    from_wallet = wallet_factory(from_wallet_group)
    to_wallet = wallet_factory(to_wallet_group)

    with pytest.raises(HTTPException) as exc:
        ts.validate_savings(from_wallet, to_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid Savings transaction!"