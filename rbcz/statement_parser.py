import re

from .statement_header_parser import StatementHeaderParser
from .account_summary_parser import AccountSummaryParser
from .account_movements_parser import AccountMovementsParser

section_regex = "^=+$"

class StatementParser(object):

    def __init__(self):
        self.parsers = [
            StatementHeaderParser(),
            AccountSummaryParser(),
            AccountMovementsParser()
        ]

    def split_into_sections(self, file_contents):

        sections = []
        current_section = []
        
        for line in file_contents:

            if re.match(section_regex, line):
                sections.append(current_section)
                current_section = []
                continue

            current_section.append(line)
            
        return sections
        
    def Parse(self, file_contents):

        parser_idx = 0
        sections = self.split_into_sections(file_contents)

        statement = Statment()
        
        for section in sections:
            for parser in parsers[parser_idx:]:
                try:
                    parser.Parse(statement, section)
                    parser_idx += 1
                except:
                    pass

        return statement
                
