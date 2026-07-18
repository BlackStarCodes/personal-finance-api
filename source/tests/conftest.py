import pytest
from source.models.wallet import WalletOrm
from source.models.category import CategoryOrm
from source.enums import WalletGroup, WalletType
from decimal import Decimal


@pytest.fixture
def wallet_factory():
    def create_wallet(wallet_group):
        return WalletOrm(
            name = wallet_group.value,
            type = WalletType.BANK,
            currency = "INR",
            balance = Decimal("1000.00"),
            wallet_group = wallet_group,
        )
    return create_wallet


@pytest.fixture
def category_factory():
    def create_category(category_type):
        return CategoryOrm(
            name = category_type.value,
            type = category_type,
        )
    return create_category