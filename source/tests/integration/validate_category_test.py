import pytest
from fastapi import HTTPException
from source.models.category import CategoryOrm
import source.services.transaction_service as ts


def test_category_returns_user_category(
    db_session,
    db_user,
    db_category
):
    category = ts.validate_category(
        user_id= db_user.id,
        category_id= db_category.id,
        session= db_session
    )

    assert category.id  == db_category.id
    assert category.user_id == db_user.id
    assert category.name == "Food"


def test_category_rejects_another_user_category(
    db_session,
    db_user,
    db_other_category
):
    with pytest.raises(HTTPException) as exc:
        ts.validate_category(
            user_id= db_user.id,
            category_id= db_other_category.id,
            session= db_session
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Category Not Found!"


def test_category_rejects_nonexistent_category(
    db_session,
    db_user
):
    with pytest.raises(HTTPException) as exc:
        ts.validate_category(
            user_id=db_user.id,
            category_id= 4995255,
            session= db_session
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Category Not Found!"
