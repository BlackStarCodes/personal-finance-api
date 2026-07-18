import pytest
from fastapi import HTTPException
import source.services.transaction_service as ts
from source.enums import WalletGroup


def test_emergency_fund_requires_source_wallet(wallet_factory):
    emergency_fund_wallet = wallet_factory(WalletGroup.EMERGENCY_FUND)
    with pytest.raises(HTTPException) as exc:
        ts.validate_emergency_fund(from_wallet=None, to_wallet=emergency_fund_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Emergency Fund transaction needs a source wallet!"


def test_emergency_fund_requires_destination_wallet(wallet_factory):
    emergency_fund_wallet = wallet_factory(WalletGroup.EMERGENCY_FUND)
    with pytest.raises(HTTPException) as exc:
        ts.validate_emergency_fund(from_wallet=emergency_fund_wallet, to_wallet=None)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Emergency Fund transaction needs a destination wallet!"


VALID_PAIRS = [
        (WalletGroup.AVAILABLE, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.UNASSIGNED, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.AVAILABLE),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.UNASSIGNED),
        (WalletGroup.INVESTMENT, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.SAVINGS, WalletGroup.EMERGENCY_FUND),]

@pytest.mark.parametrize("from_wallet_group, to_wallet_group", VALID_PAIRS)

def test_emergency_fund_accepts_valid_wallet_groups(from_wallet_group, to_wallet_group, wallet_factory):
     
     from_wallet = wallet_factory(from_wallet_group)
     to_wallet = wallet_factory(to_wallet_group)

     ts.validate_emergency_fund(from_wallet, to_wallet)



INVALID_PAIRS = [
        (WalletGroup.DEBT, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.DEBT),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.SAVINGS),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.INVESTMENT),
        (WalletGroup.AVAILABLE, WalletGroup.UNASSIGNED),
        (WalletGroup.INVESTMENT, WalletGroup.SAVINGS),
        (WalletGroup.EMERGENCY_FUND, WalletGroup.EMERGENCY_FUND),
        (WalletGroup.UNASSIGNED, WalletGroup.UNASSIGNED),
        (WalletGroup.AVAILABLE, WalletGroup.SAVINGS),
        (WalletGroup.UNASSIGNED, WalletGroup.DEBT),
        (WalletGroup.INVESTMENT, WalletGroup.AVAILABLE),
        (WalletGroup.DEBT, WalletGroup.INVESTMENT),
        ]


@pytest.mark.parametrize("from_wallet_group, to_wallet_group", INVALID_PAIRS)

def test_emergency_fund_rejects_invalid_wallet_groups(from_wallet_group, to_wallet_group, wallet_factory):
     
    from_wallet = wallet_factory(from_wallet_group)
    to_wallet = wallet_factory(to_wallet_group)

    with pytest.raises(HTTPException) as exc:
        ts.validate_emergency_fund(from_wallet, to_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid Emergency Fund transaction!"