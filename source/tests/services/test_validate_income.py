import pytest
from fastapi import HTTPException
import source.services.transaction_service as ts


def test_income_source_cannot_have_source_wallet(available_wallet, unassigned_wallet):
    with pytest.raises(HTTPException) as exc:
        ts.validate_income(available_wallet, unassigned_wallet)

    assert exc.value.status_code ==  400
    assert exc.value.detail == "Income transaction cannot have a source wallet!"


def test_income_requires_destination_wallet():
    with pytest.raises(HTTPException) as exc:
        ts.validate_income(from_wallet=None, to_wallet=None)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Income transaction needs a destination wallet!"


def test_income_accepts_available(available_wallet):
    ts.validate_income(from_wallet=None, to_wallet=available_wallet)


def test_income_accepts_unassigned(unassigned_wallet):
    ts.validate_income(from_wallet=None, to_wallet=unassigned_wallet)


def test_income_rejects_savings(savings_wallet):
    with pytest.raises(HTTPException) as exc:
        ts.validate_income(from_wallet=None, to_wallet=savings_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Income transaction can only go to Available or Unassigned Wallets!"


def test_income_rejects_emergency_fund(emergency_wallet):
    with pytest.raises(HTTPException) as exc:
        ts.validate_income(from_wallet=None, to_wallet=emergency_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Income transaction can only go to Available or Unassigned Wallets!"


def test_income_rejects_investment(investment_wallet):
    with pytest.raises(HTTPException) as exc:
        ts.validate_income(from_wallet=None, to_wallet=investment_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Income transaction can only go to Available or Unassigned Wallets!"


def test_income_rejects_debt(debt_wallet):
    with pytest.raises(HTTPException) as exc:
        ts.validate_income(from_wallet=None, to_wallet=debt_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Income transaction can only go to Available or Unassigned Wallets!"