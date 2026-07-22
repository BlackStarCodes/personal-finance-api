import pytest
from fastapi import HTTPException
import source.services.transaction_service as ts


def test_validate_wallets_returns_user_wallet(
    db_session,
    db_user,
    db_wallet
): 
    to_wallet, from_wallet = ts.validate_wallets(
        user_id=db_user.id,
        to_wallet_id=db_wallet.id,
        from_wallet_id=None,
        session=db_session,
    )

    assert to_wallet.id == db_wallet.id
    assert from_wallet is None


def test_validate_wallets_rejects_to_wallet_of_another_user(
    db_session,
    db_user,
    db_other_wallet
): 
    with pytest.raises(HTTPException) as exc:

        ts.validate_wallets(
            user_id=db_user.id,
            to_wallet_id=db_other_wallet.id,
            from_wallet_id=None,
            session=db_session,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Destination wallet not found."


def test_validate_wallets_rejects_from_wallet_of_another_user(
    db_session,
    db_user,
    db_other_wallet
): 
    with pytest.raises(HTTPException) as exc:

        ts.validate_wallets(
            user_id=db_user.id,
            from_wallet_id=db_other_wallet.id,
            to_wallet_id=None,
            session=db_session,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Source wallet not found."


def test_validates_wallets_rejects_same_to_and_from_wallet(
    db_session,
    db_user,
    db_wallet
):
    with pytest.raises(HTTPException) as exc:

        ts.validate_wallets(
            user_id=db_user.id,
            from_wallet_id=db_wallet.id,
            to_wallet_id=db_wallet.id,
            session=db_session,
        )

    assert exc.value.status_code == 400
    assert exc.value.detail == "Source and destination wallet cannot be the same!"


def test_validate_wallets_returns_both_user_wallet(
    db_session,
    db_user,
    db_wallet,
    db_second_wallet
): 
    to_wallet, from_wallet = ts.validate_wallets(
        user_id=db_user.id,
        to_wallet_id=db_wallet.id,
        from_wallet_id=db_second_wallet.id,
        session=db_session,
    )

    assert to_wallet.id == db_wallet.id
    assert from_wallet.id == db_second_wallet.id


