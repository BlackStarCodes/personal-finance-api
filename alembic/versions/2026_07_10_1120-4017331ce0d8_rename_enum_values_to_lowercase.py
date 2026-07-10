"""rename enum values to lowercase

Revision ID: 4017331ce0d8
Revises: 2ea4b06af863
Create Date: 2026-07-10 11:20:21.063479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4017331ce0d8'
down_revision: Union[str, Sequence[str], None] = '2ea4b06af863'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        ALTER TYPE transactionstatus
        RENAME VALUE 'PENDING' TO 'pending';
        """
    )

    op.execute(
        """
        ALTER TYPE transactionstatus
        RENAME VALUE 'COMPLETED' TO 'completed';
        """
    )

    op.execute(
        """
        ALTER TYPE transactionstatus
        RENAME VALUE 'CANCELLED' TO 'cancelled';
        """
    )

    op.execute(
        """
        ALTER TYPE transactionstatus
        RENAME VALUE 'FAILED' TO 'failed';
        """
    )
    
    op.execute(
        """
        ALTER TYPE transactionmedium
        RENAME VALUE 'CASH' TO 'cash';
        """
    )

    op.execute(
        """
        ALTER TYPE transactionmedium
        RENAME VALUE 'UPI' TO 'upi';
        """
    )

    op.execute(
        """
        ALTER TYPE transactionmedium
        RENAME VALUE 'DEBIT_CARD' TO 'debit_card';
        """
    )

    op.execute(
        """
        ALTER TYPE transactionmedium
        RENAME VALUE 'CREDIT_CARD' TO 'credit_card';
        """
    )
    op.execute(
    """
    ALTER TYPE transactionmedium
    RENAME VALUE 'NET_BANKING' TO 'net_banking';
    """
    )
    op.execute(
    """
    ALTER TYPE transactionmedium
    RENAME VALUE 'APP' TO 'app';
    """
    )   
    op.execute(
    """
    ALTER TYPE transactionmedium
    RENAME VALUE 'GIFT_CARD' TO 'gift_card';
    """
    )
    op.execute(
    """
    ALTER TYPE categorytype
    RENAME VALUE 'INCOME' TO 'income';
    """
    )
    op.execute(
    """
    ALTER TYPE categorytype
    RENAME VALUE 'EXPENSE' TO 'expense';
    """
    )
    op.execute(
    """
    ALTER TYPE categorytype
    RENAME VALUE 'SAVINGS' TO 'savings';
    """
    )
    op.execute(
    """
    ALTER TYPE categorytype
    RENAME VALUE 'EMERGENCY_FUND' TO 'emergency_fund';
    """
    )
    op.execute(
    """
    ALTER TYPE categorytype
    RENAME VALUE 'INVESTMENT' TO 'investment';
    """
    )
    op.execute(
    """
    ALTER TYPE categorytype
    RENAME VALUE 'TRANSFER' TO 'transfer';
    """
    )
    op.execute(
    """
    ALTER TYPE wallettype
    RENAME VALUE 'CASH' TO 'cash';
    """
    )
    op.execute(
    """
    ALTER TYPE wallettype
    RENAME VALUE 'BANK' TO 'bank';
    """
    )

    op.execute(
        """
        ALTER TYPE wallettype
        RENAME VALUE 'CREDIT_CARD' TO 'credit_card';
        """
        )

    op.execute(
        """
        ALTER TYPE wallettype
        RENAME VALUE 'CRYPTO' TO 'crypto';
        """
        )

    op.execute(
        """
        ALTER TYPE wallettype
        RENAME VALUE 'INVESTMENT' TO 'investment';
        """
        )

    op.execute(
        """
        ALTER TYPE wallettype
        RENAME VALUE 'OTHER' TO 'other';
        """
        )

    op.execute(
        """
        ALTER TYPE wallettype
        RENAME VALUE 'EMERGENCY_FUND' TO 'emergency_funds';
        """
        )




def downgrade() -> None:
    """Downgrade schema."""
    pass
