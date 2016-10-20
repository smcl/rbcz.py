import re
from .utils import to_long_date

statement_number_regex = "Bank statement No. (\d+)"
date_regex = "\d\d\.\d\d\.\d\d\d\d"
for_period_regex = "For period (%s)/(%s)" % (date_regex, date_regex)
colon_delimit_regex = "(.*)\:\s*([\w\d].*)"

account_name_label = "Name of account"
account_number_label = "Account number"
iban_label = "IBAN"
currency_label = "Currency"


class StatementHeaderParser(object):

    def Parse(self, statement, section):

        parsers = [
            self.parse_statement_number,
            self.parse_from_to,
            self.parse_assign
        ]

        for line in section:
            if not line:
                continue

            for parser in parsers:
                if parser(statement, line):
                    break

    def parse_statement_number(self, statement, line):
        parsed_stmt_number = re.match(statement_number_regex, line)

        if parsed_stmt_number:
            statement.number = int(parsed_stmt_number.group(1))
            return True
        return False

    def parse_from_to(self, statement, line):
        parsed_dates = re.match(for_period_regex, line)
        if parsed_dates:
            (from_date, to_date) = parsed_dates.groups()
            statement.from_date = to_long_date(from_date)
            statement.to_date = to_long_date(to_date)
            return True
        return False

    def parse_assign(self, statement, line):

        parsed_assign = re.match(colon_delimit_regex, line)
        if parsed_assign:
            (label, value) = parsed_assign.groups()

            if (label == account_name_label):
                statement.account_name = value
            elif (label == account_number_label):
                statement.account_number = value
            elif (label == iban_label):
                statement.iban = value
            elif (label == currency_label):
                statement.currency = value
        return bool(parsed_assign)
