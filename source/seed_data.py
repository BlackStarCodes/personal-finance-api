from .enums import CategoryType

"""
class CategoryType(str, Enum):
    INCOME = 'income'
    EXPENSE = 'expense'
    SAVINGS = 'savings'
    EMERGENCY_FUND = 'emergency_fund'
    INVESTMENT = 'investment'
    TRANSFER = 'transfer'
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
    ]

