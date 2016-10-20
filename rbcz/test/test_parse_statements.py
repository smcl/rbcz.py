import unittest2
from rbcz import rbcz
from datetime import datetime
from decimal import Decimal

expected_statement_number = 8
expected_period_start = datetime(2016, 8, 1)
expected_period_end = datetime(2016, 8, 31)
expected_account_name = "Test McTestman"
expected_account_number = "2000145399/5500"
expected_iban = "CZ6508000000192000145399"
expected_currency = "CZK"
expected_opening_balance = Decimal(100000)
expected_income = Decimal(50000)
expected_expense = Decimal(-30000)
expected_closing_balance = Decimal(120000)
expected_blocked = Decimal(0)
expected_receivable = Decimal(0)
expected_available = Decimal(120000)


class ParseStatementsTest(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        self.statement = rbcz.read_statements(
            ["./rbcz/test/test_stmt.txt", "./rbcz/test/test_stmt_2.txt"])[0]
        super(ParseStatementsTest, self).__init__(*args, **kwargs)

    def test_count_movements(self):
        self.assertEqual(len(self.statement.movements), 4)

    def test_statement_number(self):
        self.assertEqual(self.statement.number, expected_statement_number)

    def test_start_period(self):
        self.assertEqual(self.statement.from_date, expected_period_start)

    def test_end_period(self):
        self.assertEqual(self.statement.to_date, expected_period_end)

    def test_account_name(self):
        self.assertEqual(self.statement.account_name, expected_account_name)

    def test_account_number(self):
        self.assertEqual(self.statement.account_number,
                         expected_account_number)

    def test_iban(self):
        self.assertEqual(self.statement.iban, expected_iban)

    def test_currency(self):
        self.assertEqual(self.statement.currency, expected_currency)

    def test_opening_balance(self):
        self.assertEqual(expected_opening_balance,
                         self.statement.opening_balance)

    def test_income(self):
        self.assertEqual(expected_income, self.statement.income)

    def test_expense(self):
        self.assertEqual(expected_expense, self.statement.expenses)

    def test_closing_balance(self):
        self.assertEqual(expected_closing_balance,
                         self.statement.closing_balance)

    def test_blocked(self):
        self.assertEqual(expected_blocked, self.statement.blocked)

    def test_receivable(self):
        self.assertEqual(expected_receivable, self.statement.receivable)

    def test_available(self):
        self.assertEqual(expected_available, self.statement.available_balance)
