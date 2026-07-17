import pytest
from fastapi import HTTPException
import source.services.transaction_service as ts



def test_expense_cannot_have_destination_wallet(available_wallet):
    with pytest.raises(HTTPException) as exc:
        ts.validate_expense(from_wallet=available_wallet, to_wallet=available_wallet)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Expense transaction cannot have a destination wallet!"
    

def test_expense_requires_source_wallet():
    with pytest.raises(HTTPException) as exc:
        ts.validate_expense(from_wallet=None, to_wallet=None)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Expense transaction needs a source wallet!"


def test_expense_accepts_available(available_wallet):
    ts.validate_expense(from_wallet=available_wallet, to_wallet=None)


def test_expense_accepts_unassigned(unassigned_wallet):
    ts.validate_expense(from_wallet=unassigned_wallet, to_wallet=None)


def test_expense_accepts_debt(debt_wallet):
    ts.validate_expense(from_wallet=debt_wallet, to_wallet=None)    


def test_expense_rejects_savings(savings_wallet):
    with pytest.raises(HTTPException) as exc:
        ts.validate_expense(from_wallet=savings_wallet, to_wallet=None)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Can only spend from available, unassigned, debt wallets!"


def test_expense_rejects_emergency_fund(emergency_wallet):
    with pytest.raises(HTTPException) as exc:
        ts.validate_expense(from_wallet=emergency_wallet, to_wallet=None)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Can only spend from available, unassigned, debt wallets!"


def test_expense_rejects_investment(investment_wallet):
    with pytest.raises(HTTPException) as exc:
        ts.validate_expense(from_wallet=investment_wallet, to_wallet=None)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Can only spend from available, unassigned, debt wallets!"

