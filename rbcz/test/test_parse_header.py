import unittest2
from ..statement_header_parser import StatementHeaderParser
from ..statement import Statement
from ..utils import to_long_date

# flake8: noqa
statement_header = """


Raiffeisenbank a.s. 
Bank statement No. 8
For period 01.08.2016/31.08.2016

Name of account: Test McTestman
Account number:  2000145399/5500
IBAN:            CZ6508000000192000145399
Currency:        CZK






""".split("\n")

expected_statement_number = 8
expected_period_start = to_long_date("01.08.2016")
expected_period_end = to_long_date("31.08.2016")
expected_account_name = "Test McTestman"
expected_account_number = "2000145399/5500"
expected_iban = "CZ6508000000192000145399"
expected_currency = "CZK"

class StatementHeaderTest(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        self.statement = Statement()
        StatementHeaderParser().Parse(self.statement, statement_header)
        super(StatementHeaderTest, self).__init__(*args, **kwargs)

    def test_statement_number(self):
        self.assertEqual(self.statement.number, expected_statement_number)
    
    def test_start_period(self):
        self.assertEqual(self.statement.from_date, expected_period_start)

    def test_end_period(self):
        self.assertEqual(self.statement.to_date, expected_period_end)

    def test_account_name(self):
        self.assertEqual(self.statement.account_name, expected_account_name)

    def test_account_number(self):
        self.assertEqual(self.statement.account_number, expected_account_number)

    def test_iban(self):
        self.assertEqual(self.statement.iban, expected_iban)

    def test_currency(self):
        self.assertEqual(self.statement.currency, expected_currency)
    
