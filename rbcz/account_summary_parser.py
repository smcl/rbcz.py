import re
from .utils import (
    to_decimal,
    money_regex
)

# parse the account summary - which will look something like this:

"""
Beginning balance                                                                 0.00
Income                                               1 000.00                 1 000.00
Expense                                                  0.00                     0.00
Ending balance                                                                1 000.00
Of which, blocked                                                                 0.00
Receivables past due                                                              0.00
Available balance                                                             1 000.00
"""

# pretty heavy on the regexes - maybe need to think about using ply (python lex/yacc)

opening_regex = r"Beginning balance\s+(%s)" % (money_regex)
income_regex = r"Income\s+(%s)\s+(%s)" % (money_regex, money_regex)
expenses_regex = r"Expense\s+(%s)\s+(%s)" % (money_regex, money_regex)
closing_regex = r"Ending balance\s+(%s)" % (money_regex)
blocked_regex = r"Of which, blocked\s+(%s)" % (money_regex)
receivable_regex = r"Receivables past due\s+(%s)" % (money_regex)
available_regex = r"Available balance\s+(%s)" % (money_regex)

from pprint import pprint

class AccountSummaryParser(object):

    def Parse(self, statement, section):

        parsers = [
            self.parse_opening,
            self.parse_income,
            self.parse_expenses,
            self.parse_closing,
            self.parse_blocked,
            self.parse_due
        ]

        for line in section:
            #print "\"" + line + "\""
            
            if not line:
                continue

            for parser in parsers:
                if parser(statement, line):
                    break
        
    def parse_opening(self, statement, line):
        parsed_opening = re.match(opening_regex, line)
        if parsed_opening:
            statement.opening_balance = to_decimal(parsed_opening.group(1))
            return True
        return False

    def parse_income(self, statement, line):
        parsed_income = re.match(income_regex, line)
        if parsed_income:
            #statement.ytd_income = to_decimal(parsed_income.group(1))
            statement.income = to_decimal(parsed_income.group(2))
            return True
        return False

    def parse_expenses(self, statement, line):
        parsed_expenses = re.match(expenses_regex, line)
        if parsed_expenses:
            #statement.ytd_expenses = to_decimal(parsed_expenses.group(1))
            statement.expenses = to_decimal(parsed_expenses.group(2))
            return True
        return False
    
    def parse_closing(self, statement, line):
        parsed_closing = re.match(closing_regex, line)
        if parsed_closing:
            statement.closing_balance = to_decimal(parsed_closing.group(1))
            return True
        return False

    def parse_blocked(self, statement, line):
        parsed_blocked = re.match(blocked_regex, line)
        if parsed_blocked:
            statement.blocked = to_decimal(parsed_blocked.group(1))
            return True
        return False

    def parse_due(self, statement, line):
        parsed_receivable = re.match(receivable_regex, line)
        if parsed_receivable:
            statement.receivable = to_decimal(parsed_receivable.group(1))
            return True
        return False

    def parse_available(self, statement, line):
        parsed_available = re.match(available_regex, line)
        if parsed_available:
            statement.available_balance = to_decimal(parsed_available.group(1))
            return True
        return False
