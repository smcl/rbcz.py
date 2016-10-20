import re
from .utils import (
    to_decimal,
    money_regex
)


opening_regex = r"Beginning balance\s+(%s)" % (money_regex)
income_regex = r"Income\s+(%s)\s+(%s)" % (money_regex, money_regex)
expenses_regex = r"Expense\s+(%s)\s+(%s)" % (money_regex, money_regex)
closing_regex = r"Ending balance\s+(%s)" % (money_regex)
blocked_regex = r"Of which, blocked\s+(%s)" % (money_regex)
receivable_regex = r"Receivables past due\s+(%s)" % (money_regex)
available_regex = r"Available balance\s+(%s)" % (money_regex)


class AccountSummaryParser(object):

    def Parse(self, statement, section):

        parsers = [
            self.parse_opening,
            self.parse_income,
            self.parse_expenses,
            self.parse_closing,
            self.parse_blocked,
            self.parse_due,
            self.parse_available
        ]

        for line in section:
            if not line:
                continue

            for parser in parsers:
                if parser(statement, line):
                    break

    def parse_opening(self, statement, line):
        opening = self.parse_summary_line(opening_regex, line, 1)
        if opening:
            statement.opening_balance = to_decimal(opening)
        return bool(opening)

    def parse_income(self, statement, line):
        income = self.parse_summary_line(income_regex, line, 2)
        if income:
            statement.income = to_decimal(income)
        return bool(income)

    def parse_expenses(self, statement, line):
        expenses = self.parse_summary_line(expenses_regex, line, 2)
        if expenses:
            statement.expenses = to_decimal(expenses)
        return bool(expenses)

    def parse_closing(self, statement, line):
        closing = self.parse_summary_line(closing_regex, line, 1)
        if closing:
            statement.closing_balance = to_decimal(closing)
        return bool(closing)

    def parse_blocked(self, statement, line):
        blocked = self.parse_summary_line(blocked_regex, line, 1)
        if blocked:
            statement.blocked = to_decimal(blocked)
        return bool(blocked)

    def parse_due(self, statement, line):
        receivable = self.parse_summary_line(receivable_regex, line, 1)
        if receivable:
            statement.receivable = to_decimal(receivable)

        return bool(receivable)

    def parse_available(self, statement, line):
        available_balance = self.parse_summary_line(available_regex, line, 1)
        if available_balance:
            statement.available_balance = to_decimal(available_balance)

        return bool(available_balance)

    def parse_summary_line(self, regex, line, group_index):
        regex_result = re.match(regex, line)

        if (regex_result):
            return regex_result.group(group_index)

        return None
