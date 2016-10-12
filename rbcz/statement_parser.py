import re

from .statement_header_parser import StatementHeaderParser
from .account_summary_parser import AccountSummaryParser
from .account_movements_parser import AccountMovementsParser

from .statement import *

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
        
        for raw_line in file_contents:
            line = raw_line.strip()
            
            if re.match(section_regex, line):
                if len(current_section) > 3 and not self.skip_section(current_section):
                    sections.append(current_section)
                current_section = []
                continue

            current_section.append(line)

        if len(current_section) > 3 and not self.skip_section(current_section):
            sections.append(current_section)
            
        return sections

    def skip_section(self, section):
        if (len(section) <= 1):
            return True

        if section[0] == "Message for client":
            return True

        return False
    
    def Parse(self, file_contents):

        parser_idx = 0
        sections = self.split_into_sections(file_contents)
        statement = Statment()
        
        for section in sections:
            for parser in self.parsers[parser_idx:]:
                parser.Parse(statement, section)
                parser_idx += 1
                break
                
        return statement
                
