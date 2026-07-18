import pytest
from fastapi import HTTPException
import source.services.transaction_service as ts
from source.enums import WalletGroup


def test_investment_requires_source_wallet(wallet_factory):
    investment_wallet = wallet_factory(WalletGroup.INVESTMENT)
    with pytest.raises(HTTPException) as exc:
        ts.validate_investment(from_wallet=None, to_wallet=investment_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Investment transaction needs a source wallet!"


def test_investment_requires_destination_wallet(wallet_factory):
    investment_wallet = wallet_factory(WalletGroup.INVESTMENT)
    with pytest.raises(HTTPException) as exc:
        ts.validate_investment(from_wallet=investment_wallet, to_wallet=None)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Investment transaction needs a destination wallet!"


VALID_PAIRS = [
        (WalletGroup.AVAILABLE, WalletGroup.INVESTMENT),
        (WalletGroup.UNASSIGNED, WalletGroup.INVESTMENT),
        (WalletGroup.INVESTMENT, WalletGroup.AVAILABLE),
        (WalletGroup.INVESTMENT, WalletGroup.UNASSIGNED),
        (WalletGroup.INVESTMENT, WalletGroup.INVESTMENT),
        (WalletGroup.SAVINGS, WalletGroup.INVESTMENT),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.INVESTMENT),]

@pytest.mark.parametrize("from_wallet_group, to_wallet_group", VALID_PAIRS)

def test_investment_accepts_valid_wallet_groups(from_wallet_group, to_wallet_group, wallet_factory):
     
    from_wallet = wallet_factory(from_wallet_group)
    to_wallet = wallet_factory(to_wallet_group)

    ts.validate_investment(from_wallet, to_wallet)



INVALID_PAIRS = [
        (WalletGroup.DEBT, WalletGroup.SAVINGS),
        (WalletGroup.INVESTMENT, WalletGroup.DEBT),
        (WalletGroup.INVESTMENT, WalletGroup.SAVINGS),
        (WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED),
        (WalletGroup.INVESTMENT, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.SAVINGS),
        (WalletGroup.UNASSIGNED, WalletGroup.UNASSIGNED),
        (WalletGroup.AVAILABLE, WalletGroup.SAVINGS),
        (WalletGroup.UNASSIGNED, WalletGroup.DEBT),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.AVAILABLE),
        (WalletGroup.DEBT, WalletGroup.INVESTMENT),
        ]


@pytest.mark.parametrize("from_wallet_group, to_wallet_group", INVALID_PAIRS)

def test_investment_rejects_invalid_wallet_groups(from_wallet_group, to_wallet_group, wallet_factory):
     
    from_wallet = wallet_factory(from_wallet_group)
    to_wallet = wallet_factory(to_wallet_group)

    with pytest.raises(HTTPException) as exc:
        ts.validate_investment(from_wallet, to_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid Investment transaction!"