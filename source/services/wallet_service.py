from source.seed_data import DEFAULT_WALLETS
from source.models.wallet import WalletOrm



def seed_default_wallets(user_id: int, session):
    for wallet in DEFAULT_WALLETS:
        session.add(WalletOrm(
            user_id=user_id,
            name = wallet['name'],
            type = wallet['type'],
            currency = wallet['currency'],
            balance = wallet['balance'],
            wallet_group = wallet['wallet_group'],
            is_default = True,
        ))

    session.flush()