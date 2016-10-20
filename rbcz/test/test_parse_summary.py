import unittest2
from ..account_summary_parser import AccountSummaryParser
from ..statement import Statement
from decimal import Decimal

# flake8: noqa
account_summary = """
Beginning balance                                                           100 000.00
Income                                             400 000.00                50 000.00
Expense                                           -300 000.00               -30 000.00
Ending balance                                                              120 000.00
Of which, blocked                                                                 0.00
Receivables past due                                                              0.00
Available balance                                                           120 000.00
""".split("\n")

expected_opening_balance = Decimal(100000)
expected_income = Decimal(50000)
expected_expense = Decimal(-30000)
expected_closing_balance = Decimal(120000)
expected_blocked = Decimal(0)
expected_receivable = Decimal(0)
expected_available = Decimal(120000)

class AccountSummaryTest(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        self.statement = Statement()
        AccountSummaryParser().Parse(self.statement, account_summary)
        super(AccountSummaryTest, self).__init__(*args, **kwargs)

    def test_opening_balance(self):
        self.assertEqual(expected_opening_balance, self.statement.opening_balance)
    
    def test_income(self):
        self.assertEqual(expected_income, self.statement.income)

    def test_expense(self):
        self.assertEqual(expected_expense, self.statement.expenses)

    def test_closing_balance(self):
        self.assertEqual(expected_closing_balance, self.statement.closing_balance)

    def test_blocked(self):
        self.assertEqual(expected_blocked, self.statement.blocked)

    def test_receivable(self):
        self.assertEqual(expected_receivable, self.statement.receivable)

    def test_available(self):
        self.assertEqual(expected_available, self.statement.available_balance)
