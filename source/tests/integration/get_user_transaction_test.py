import pytest 
from fastapi import HTTPException
import source.services.transaction_service as ts
from decimal import Decimal 


def test_get_user_transaction_returns_user_transaction(
    db_session,
    db_user,
    db_transaction
):
    
    transaction = ts.get_user_transaction(
        transaction_id=db_transaction.id,
        user_id=db_user.id,
        session=db_session,
    )

    assert transaction.id == db_transaction.id
    assert transaction.name == "Test Transfer"
    assert transaction.amount == Decimal("100") 


def test_get_user_transaction_rejects_another_user(
    db_session,
    db_other_user,
    db_transaction
):
    with pytest.raises(HTTPException) as exc:
        ts.get_user_transaction(
            transaction_id= db_transaction.id,
            user_id= db_other_user.id,
            session=db_session
        )
    
    assert exc.value.status_code == 404
    assert exc.value.detail == "Transaction Not Found!"


def test_get_user_transaction_rejects_nonexistent_transaction(
    db_session,
    db_user,
):
    with pytest.raises(HTTPException) as exc:
        ts.get_user_transaction(
            transaction_id= 9999999,
            user_id= db_user.id,
            session=db_session
        )
    
    assert exc.value.status_code == 404
    assert exc.value.detail == "Transaction Not Found!"


def test_get_user_transaction_returns_income_transaction(
    db_session,
    db_income_transaction,
    db_user,
):
    transaction = ts.get_user_transaction(
        transaction_id = db_income_transaction.id,
        user_id = db_user.id,
        session= db_session,
    )

    assert transaction.id == db_income_transaction.id
    assert transaction.name == "Test Income"


def test_get_user_transaction_returns_expense_transaction(
    db_session,
    db_expense_transaction,
    db_user,
):
    transaction = ts.get_user_transaction(
        transaction_id = db_expense_transaction.id,
        user_id = db_user.id,
        session= db_session,
    )

    assert transaction.id == db_expense_transaction.id
    assert transaction.name == "Test Expense"