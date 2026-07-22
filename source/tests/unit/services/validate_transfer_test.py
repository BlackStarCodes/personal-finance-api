import pytest
from fastapi import HTTPException
import source.services.transaction_service as ts
from source.enums import WalletGroup


def test_transfer_requires_source_wallet(wallet_factory):
    available_wallet = wallet_factory(WalletGroup.AVAILABLE)
    with pytest.raises(HTTPException) as exc:
        ts.validate_transfer(from_wallet=None, to_wallet=available_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Transfer transaction needs a source wallet!"


def test_transfer_requires_destination_wallet(wallet_factory):
    available_wallet = wallet_factory(WalletGroup.AVAILABLE)
    with pytest.raises(HTTPException) as exc:
        ts.validate_transfer(from_wallet=available_wallet, to_wallet=None)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Transfer transaction needs a destination wallet!"




VALID_PAIRS = [
        (WalletGroup.AVAILABLE, WalletGroup.AVAILABLE),
        (WalletGroup.UNASSIGNED, WalletGroup.UNASSIGNED),
        (WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED),
        (WalletGroup.UNASSIGNED, WalletGroup.AVAILABLE),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.SAVINGS, WalletGroup.SAVINGS),
        ]

@pytest.mark.parametrize("from_wallet_group, to_wallet_group", VALID_PAIRS)

def test_transfer_accepts_valid_wallet_groups(from_wallet_group, to_wallet_group, wallet_factory):
     
    from_wallet = wallet_factory(from_wallet_group)
    to_wallet = wallet_factory(to_wallet_group)

    ts.validate_transfer(from_wallet, to_wallet)



INVALID_PAIRS = [
        (WalletGroup.EMERGENCY_FUND, WalletGroup.SAVINGS),
        (WalletGroup.INVESTMENT, WalletGroup.AVAILABLE),
        (WalletGroup.SAVINGS, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.DEBT, WalletGroup.UNASSIGNED),
        (WalletGroup.UNASSIGNED, WalletGroup.INVESTMENT),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.UNASSIGNED),
        (WalletGroup.UNASSIGNED, WalletGroup.DEBT),
        (WalletGroup.AVAILABLE, WalletGroup.SAVINGS),
        (WalletGroup.UNASSIGNED, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.AVAILABLE),
        (WalletGroup.SAVINGS, WalletGroup.INVESTMENT),
        ]


@pytest.mark.parametrize("from_wallet_group, to_wallet_group", INVALID_PAIRS)

def test_transfer_rejects_invalid_wallet_groups(from_wallet_group, to_wallet_group, wallet_factory):
     
    from_wallet = wallet_factory(from_wallet_group)
    to_wallet = wallet_factory(to_wallet_group)

    with pytest.raises(HTTPException) as exc:
        ts.validate_transfer(from_wallet, to_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid Transfer Transaction!"