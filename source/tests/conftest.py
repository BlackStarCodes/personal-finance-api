import pytest
from source.models.wallet import WalletOrm
from source.enums import WalletGroup, WalletType
from decimal import Decimal


@pytest.fixture
def available_wallet():
    return WalletOrm(
        name = "Available",
        type =  WalletType.BANK,
        currency = 'INR',
        balance = Decimal("1000.00"),
        wallet_group = WalletGroup.AVAILABLE
    )

@pytest.fixture
def unassigned_wallet():
    return WalletOrm(
        name = "Unassigned",
        type =  WalletType.CASH,
        currency = 'INR',
        balance = Decimal("1000.00"),
        wallet_group = WalletGroup.UNASSIGNED
    )

@pytest.fixture
def savings_wallet():
    return WalletOrm(
        name = "Savings",
        type =  WalletType.BANK,
        currency = 'INR',
        balance = Decimal("1000.00"),
        wallet_group = WalletGroup.SAVINGS
    )


@pytest.fixture
def emergency_wallet():
    return WalletOrm(
        name = "Emergency Fund",
        type =  WalletType.BANK,
        currency = 'INR',
        balance = Decimal("1000.00"),
        wallet_group = WalletGroup.EMERGENCY_FUND
    )

@pytest.fixture
def investment_wallet():
    return WalletOrm(
        name = "Investments",
        type =  WalletType.BANK,
        currency = 'INR',
        balance = Decimal("1000.00"),
        wallet_group = WalletGroup.INVESTMENT
    )

@pytest.fixture
def debt_wallet():
    return WalletOrm(
        name = "Credit Card",
        type =  WalletType.CREDIT_CARD,
        currency = 'INR',
        balance = Decimal("1000.00"),
        wallet_group = WalletGroup.DEBT
    )