import re
from utils import to_long_date

# what we're needing to do is parse a chunk of text like the following

"""
Raiffeisenbank a.s. 
Bank statement No. 8
For period 01.08.2016/31.08.2016

Name of account: Sean James McLemon
Account number: 6986230001/5500
IBAN:            CZ3555000000006986230001
Currency:        CZK
"""

# how we'll do this is
# 1. strip blank lines (there's a few)
# 2. retrieve the bank statement number
# 3. retrieve the from/to dates
# 4. pick out the values of the form "name: value" and strip() them

statement_number_regex = "Bank statement No. (\d+)"
date_regex = "\d\d\.\d\d\.\d\d\d\d"
for_period_regex = "For period (%s)/(%s)" % (date_regex, date_regex)
colon_delimit_regex = "(.*)\:(.*)"

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
            statement.number = parsed_stmt_number.group(1)
            return True
        return False

    def parse_from_to(self, statement, line):
        parsed_dates = re.match(for_period_regex, line)
        if parsed_dates:
            statement.from_date = to_long_date(parsed_dates.group(1))
            statement.to_date = to_long_date(parsed_dates.group(2))
            return True
        return False
            
    def parse_assign(self, statement, line):
        
        parsed_assign = re.match(colon_delimit_regex, line)
        if parsed_assign:
            label = parsed_assign.group(1).strip()
            value = parsed_assign.group(2).strip()

            if (label == account_name_label):
                statement.account_name = value
            elif (label == account_number_label):
                statement.account_number = value
            elif (label == iban_label):
                statement.iban = value
            elif (label == currency_label):
                statement.currency = value
            else:
                return False
            return True
        return False
    
