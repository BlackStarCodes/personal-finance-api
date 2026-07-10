from enum import Enum


class WalletType(str, Enum):
    CASH = 'cash'
    BANK = 'bank'
    CREDIT_CARD = 'credit_card'
    CRYPTO = 'crypto'
    INVESTMENT = 'investment'
    OTHER = 'other'


class CategoryType(str, Enum):
    INCOME = 'income'
    EXPENSE = 'expense'
    SAVINGS = 'savings'
    EMERGENCY_FUND = 'emergency_fund'
    INVESTMENT = 'investment'
    TRANSFER = 'transfer'


class TransactionStatus(str, Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    FAILED = 'failed'


class TransactionMedium(str, Enum):
    CASH = 'cash'
    UPI = 'upi'
    DEBIT_CARD = 'debit_card'
    CREDIT_CARD = 'credit_card'
    NET_BANKING ='net_banking'
    APP = 'app'
    GIFT_CARD = 'gift_card'


class WalletGroup(str, Enum):
    AVAILABLE = 'available'
    SAVINGS = 'savings'
    EMERGENCY_FUND = 'emergency_fund'
    INVESTMENT = 'investment'
    UNASSIGNED = 'unassigned'