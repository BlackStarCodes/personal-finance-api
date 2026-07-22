import pytest
from fastapi import HTTPException
import source.services.transaction_service as ts 
from source.enums import CategoryType, WalletGroup
from unittest.mock import Mock


@pytest.mark.parametrize(
    "category_type, validator_name",    
    [
        (CategoryType.INCOME, "validate_income"),
        (CategoryType.EXPENSE, "validate_expense"),
        (CategoryType.SAVINGS, "validate_savings"),
        (CategoryType.EMERGENCY_FUND, "validate_emergency_fund"),
        (CategoryType.INVESTMENT, "validate_investment"),
        (CategoryType.DEBT, "validate_debt"),
        (CategoryType.TRANSFER, "validate_transfer"),

    ]
)

def test_transaction_rules_uses_correct_validator(
    category_type,
    validator_name, 
    monkeypatch,
    wallet_factory, 
    ):

    available_wallet = wallet_factory(WalletGroup.AVAILABLE)
    unassigned_wallet = wallet_factory(WalletGroup.UNASSIGNED)

    mock_validator = Mock()

    monkeypatch.setattr(ts, validator_name, mock_validator)

    category = Mock()
    category.type = category_type

    ts.validate_transaction_rules(category, available_wallet, unassigned_wallet)

    mock_validator.assert_called_once_with(available_wallet, unassigned_wallet)
    

def test_transaction_rules_rejects_unknown_category_type():  
    category = Mock()
    category.type = "Unknown"

    with pytest.raises(HTTPException) as exc:
        ts.validate_transaction_rules(
            category,
            from_wallet=None,
            to_wallet=None,
        )
    
    assert exc.value.status_code == 400
    assert exc.value.detail ==  "Category type not found!"