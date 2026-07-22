import pytest
from source.models.wallet import WalletOrm
from source.models.category import CategoryOrm
from source.enums import WalletGroup, WalletType, CategoryType, TransactionMedium
from decimal import Decimal
from sqlalchemy import create_engine
from source.database import Base
from source.config import TEST_DB
from sqlalchemy.orm import Session
from source.models.user import UserOrm
from source.models.transaction import TransactionOrm
from datetime import datetime, timezone



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


test_engine = create_engine(TEST_DB)



@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(test_engine)

    yield

    Base.metadata.drop_all(test_engine)


@pytest.fixture
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)
    
    try:
        yield session
    finally:
        session.close()
        session.rollback()
        connection.close()



@pytest.fixture
def db_user(db_session):
    user = UserOrm(
        username = "testuser",
        email = "test@example.com",
        hashed_password = "Strong Password"
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def db_wallet(db_session, db_user):
    wallet = WalletOrm(
        user_id = db_user.id,
        name = "Available",
        type = WalletType.BANK,
        currency = "INR",
        balance = Decimal("1000.00"),
        wallet_group = WalletGroup.AVAILABLE,
    )

    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    return wallet


@pytest.fixture
def db_second_wallet(db_session, db_user):
    wallet = WalletOrm(
        user_id = db_user.id,
        name = "Unassigned",
        type = WalletType.BANK,
        currency = "INR",
        balance = Decimal("1000.00"),
        wallet_group = WalletGroup.UNASSIGNED,
    )

    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    return wallet


@pytest.fixture
def db_other_user(db_session):
    user = UserOrm(
        username = "otheruser",
        email = "other@example.com",
        hashed_password = "Strong Password2",
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def db_other_wallet(db_session, db_other_user):
    wallet = WalletOrm(
        user_id = db_other_user.id,
        name= "Other User Wallet",
        type = WalletType.BANK,
        currency = "INR",
        balance = Decimal("1000.00"),
        wallet_group = WalletGroup.AVAILABLE,
    )

    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)
    return wallet


@pytest.fixture
def db_category(db_session, db_user):
    category = CategoryOrm(
        user_id = db_user.id,
        name= "Food",
        type= CategoryType.EXPENSE,
    )

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    return category


@pytest.fixture
def db_other_category(db_session, db_other_user):
    category = CategoryOrm(
        user_id = db_other_user.id,
        name = "Food",
        type = CategoryType.EXPENSE
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    return category


@pytest.fixture
def db_transaction(
    db_session,
    db_user,
    db_wallet,
    db_second_wallet,
    db_category,
):
    transaction = TransactionOrm(
        name ="Test Transfer",
        from_wallet_id = db_wallet.id,
        to_wallet_id = db_second_wallet.id,
        category_id = db_category.id,
        amount = Decimal("100"),
        transaction_date = datetime.now(timezone.utc),
        transaction_medium = TransactionMedium.NET_BANKING,

    )
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)
    
    return transaction


@pytest.fixture
def db_income_transaction(
    db_session,
    db_user,
    db_wallet,
    db_category,
):
    transaction = TransactionOrm(
        name = "Test Income",
        from_wallet_id = None,
        to_wallet_id = db_wallet.id,
        category = db_category,
        amount = Decimal("1000"),
        transaction_date = datetime.now(timezone.utc),
        transaction_medium = TransactionMedium.NET_BANKING,  
    )

    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    return transaction


@pytest.fixture
def db_expense_transaction(
    db_session,
    db_user,
    db_wallet,
    db_category,
):
    transaction = TransactionOrm(
        name = "Test Expense",
        from_wallet_id = db_wallet.id,
        to_wallet_id = None,
        category = db_category,
        amount = Decimal("500"),
        transaction_date = datetime.now(timezone.utc),
        transaction_medium = TransactionMedium.NET_BANKING,  
    )

    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    return transaction