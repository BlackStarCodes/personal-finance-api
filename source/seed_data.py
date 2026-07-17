from source.enums import CategoryType, WalletGroup, WalletType


"""
For reference:
class CategoryType(str, Enum):
    INCOME = 'income'
    EXPENSE = 'expense'
    SAVINGS = 'savings'
    EMERGENCY_FUND = 'emergency_fund'
    INVESTMENT = 'investment'
    TRANSFER = 'transfer'
    

class WalletType(str, Enum):
    CASH = 'cash'
    BANK = 'bank'
    CREDIT_CARD = 'credit_card'
    CRYPTO = 'crypto'
    Brokerage = 'brokerage'
    OTHER = 'other'
    

class WalletGroup(str, Enum):
    AVAILABLE = 'available'
    SAVINGS = 'savings'
    EMERGENCY_FUND = 'emergency_fund'
    INVESTMENT = 'investment'
    UNASSIGNED = 'unassigned'
    DEBT = 'debt'
    
    """


DEFAULT_CATEGORIES = [
    {"name": "Food", "type":CategoryType.EXPENSE},
    {"name": "Salary", "type":CategoryType.INCOME},
    {"name": "Rent", "type":CategoryType.EXPENSE},
    {"name": "Commute Cost", "type":CategoryType.EXPENSE},
    {"name": "Shopping", "type":CategoryType.EXPENSE},
    {"name": "Savings", "type":CategoryType.SAVINGS},
    {"name": "Stocks", "type":CategoryType.INVESTMENT},
    {"name": "Mutual Funds", "type":CategoryType.INVESTMENT},
    {"name": "Bonds", "type":CategoryType.INVESTMENT},
    {"name": "Fixed Deposit", "type":CategoryType.INVESTMENT},
    {"name": "Gold", "type":CategoryType.INVESTMENT},
    {"name": "Medical", "type":CategoryType.EXPENSE},
    {"name": "Books", "type":CategoryType.EXPENSE},
    {"name": "Vacation", "type":CategoryType.EXPENSE},
    {"name": "Electricity", "type":CategoryType.EXPENSE},
    {"name": "Subscription", "type":CategoryType.EXPENSE},
    {"name": "Pre Booking Cost", "type":CategoryType.EXPENSE},
    {"name": "Equipment", "type":CategoryType.EXPENSE},
    {"name": "Hobby", "type":CategoryType.EXPENSE},
    {"name": "Movies", "type":CategoryType.EXPENSE},
    {"name": "Groceries", "type":CategoryType.EXPENSE},
    {"name": "Gift", "type":CategoryType.EXPENSE},
    {"name": "Gym", "type":CategoryType.EXPENSE},
    {"name": "Transfer", "type":CategoryType.TRANSFER},
    {"name": "Sent to Family", "type":CategoryType.EXPENSE},
    {"name": "Lent to Friend", "type":CategoryType.EXPENSE},
    {"name": "Internet", "type":CategoryType.EXPENSE},
    {"name": "Phone Bill", "type":CategoryType.EXPENSE},
    {"name": "Insurance", "type":CategoryType.EXPENSE},
    {"name": "Entertainment", "type":CategoryType.EXPENSE},
    {"name": "Taxes", "type":CategoryType.EXPENSE},
    {"name": "Interest Received", "type":CategoryType.INCOME},
    {"name": "Interest Paid", "type":CategoryType.EXPENSE},
    {"name": "Dividends", "type":CategoryType.INCOME},
    {"name": "Emergency Fund", "type":CategoryType.EMERGENCY_FUND},
    {"name": "Education Loan", "type":CategoryType.DEBT},
    {"name": "Credit Card", "type":CategoryType.DEBT},
    {"name": "Home Loan", "type":CategoryType.DEBT},
    {"name": "Personal Loan", "type":CategoryType.DEBT},
    {"name": "Automobile Loan", "type":CategoryType.DEBT},
    {"name": "Informal Loan", "type":CategoryType.DEBT},
    ]


DEFAULT_WALLETS = [
    {"name":"Available", "type":WalletType.BANK, "currency":"INR", "balance":0, "wallet_group":WalletGroup.AVAILABLE},
    {"name":"Unassigned", "type":WalletType.CASH, "currency":"INR", "balance":0, "wallet_group":WalletGroup.UNASSIGNED},
    {"name":"Savings", "type":WalletType.BANK, "currency":"INR", "balance":0, "wallet_group": WalletGroup.SAVINGS},
    {"name":"Emergency Fund", "type":WalletType.BANK, "currency":"INR", "balance":0, "wallet_group":WalletGroup.EMERGENCY_FUND},
    {"name":"Investments", "type":WalletType.BROKERAGE, "currency":"INR", "balance":0, "wallet_group":WalletGroup.INVESTMENT},
    {"name":"Credit Card", "type":WalletType.CREDIT_CARD, "currency":"INR", "balance":0, "wallet_group":WalletGroup.DEBT},
]