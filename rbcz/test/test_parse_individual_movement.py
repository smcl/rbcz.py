import unittest2
from pprint import pprint
from ..account_movements_parser import AccountMovementsParser
from ..statement import Statement
from datetime import datetime
from decimal import Decimal

# an example account summary
account_movement = """   2 01.08.                      11.08.                            50 000.00          
     14:47 TestCorp s.r.o                                                       
           5200011647/5500                  558        Enter transfer                 
--------------------------------------------------------------------------------------
""".split("\n")

expected_movement_number = 2
expected_date_created = datetime(2016, 8, 1)
expected_date_completed = datetime(2016, 8, 11, 14, 47)
expected_amount = Decimal(50000)
expected_payment_source =  "TestCorp s.r.o"
expected_counterparty_account_number = "5200011647/5500"
expected_transaction_type = "Enter transfer"

class AccountSummaryTest(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        self.statement = Statement()
        self.statement.from_date = datetime(2016, 1, 1) # parser takes year from this field
        AccountMovementsParser().Parse(self.statement, account_movement)

        self.assertGreaterEqual(len(self.statement.movements), 1)
        self.movement = self.statement.movements[0]
        super(AccountSummaryTest, self).__init__(*args, **kwargs)

    def test_number(self):
        self.assertEqual(expected_movement_number, self.movement.number)

    def test_amount(self):
        self.assertEqual(expected_amount, self.movement.amount)

    def test_date_created(self):
        self.assertEqual(expected_date_created, self.movement.date_created)

    def test_date_completed(self):
        self.assertEqual(expected_date_completed, self.movement.date_completed)

    def test_counterparty_account_number(self):
        self.assertEqual(expected_counterparty_account_number, self.movement.counterparty_account_number)

    def test_transaction_type(self):
        self.assertEqual(expected_transaction_type, self.movement.transaction_type)

    def test_payment_source(self):
        self.assertEqual(expected_payment_source, self.movement.payment_source)

