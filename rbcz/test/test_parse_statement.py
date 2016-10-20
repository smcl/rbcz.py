import unittest2
from rbcz import rbcz
from datetime import datetime

expected_statement_number = 8
expected_period_start = datetime(2016, 8, 1)
expected_period_end = datetime(2016, 8, 31)
expected_account_name = "Test McTestman"
expected_account_number = "2000145399/5500"
expected_iban = "CZ6508000000192000145399"
expected_currency = "CZK"


class ParseStatementTest(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        self.statement = rbcz.read_statement("./rbcz/test/test_stmt.txt")
        super(ParseStatementTest, self).__init__(*args, **kwargs)

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
