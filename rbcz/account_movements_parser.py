import re
from datetime import (
    datetime,
    timedelta
)    
from .movement import Movement
from .utils import (
    to_decimal,
    money_regex,
    to_short_date
)

# meant to parse a section like the below - lines of transactions split up
# by series of dashes

"""
   1 02.08.RB Ceska, Brno, CZE   29.07.                            -1 800.00          
     10:57 Debit Card:516872XXXXX                                                     
           8323453/5500                     1178       Withdraw from ATM              
--------------------------------------------------------------------------------------
   2 02.08.RB Ceska, Brno, CZE   31.07.                            -1 800.00          
     10:57 Debit Card:516872XXXXX                                                     
           8323453/5500                     1178       Withdraw from ATM              
--------------------------------------------------------------------------------------
   3 02.08.                      31.07.                              -617.20          
     10:57 Debit Card:516872XXXXX                                                     
           8323525/5500                     1178       Card payment                   
           Billa Namesti Svobody, Brno - Omega, CZE
--------------------------------------------------------------------------------------
"""

delimiter_regex = "^-+$"

class AccountMovementsParser(object):

    def Parse(self, statement, section):
        movements = self.split_into_movements(section)

        for movement in movements:
            if len(movement) > 1:
                m = Movement()
                self.parse_first_line(statement, m, movement[0])
                self.parse_second_line(statement, m, movement[1])
                self.parse_third_line(statement, m, movement[2])
                if (len(movement) > 3):
                    self.parse_fourth_line(statement, m, movement[3])
                statement.movements.append(m)
                
    def split_into_movements(self, section_contents):
        movements = []
        current_movement = []

        for line in section_contents:
            if re.match(delimiter_regex, line):
                movements.append(current_movement)
                current_movement = []
                continue

            current_movement.append(line)

        return movements       
    
    def parse_first_line(self, statement, movement, line):
        current_year = statement.from_date.year
        
        first_regex = r"\s*(\d+)\s+(\d\d\.\d\d)\.(.*)(\d\d\.\d\d)\.\s{5}\d?\s+(%s)" % (money_regex)

        first_match = re.match(first_regex, line)

        if first_match:
            movement.number = int(first_match.group(1))
            movement.date_completed = to_short_date(first_match.group(2), current_year)
            movement.narrative = first_match.group(3).strip()
            movement.date_deducted = to_short_date(first_match.group(4), current_year)
            movement.amount = to_decimal(first_match.group(5))
            
    def parse_second_line(self, statement, movement, line):
        second_regex = r"(\d\d\:\d\d)\s(.*)$"

        second_match = re.match(second_regex, line)

        if second_match:
            (hours, minutes) = [ int(s) for s in second_match.group(1).split(":")]
            movement.date_deducted += timedelta(hours = hours, minutes = minutes)

    def parse_third_line(self, statement, movement, line):

        third_regex = "(\d+/\d+)\s+(\d+)\s+([\w].*)$"

        third_match= re.match(third_regex, line)
        
        if third_match:
            account_number, ssvscs, transaction_type = third_match.groups()

            movement.counterparty_account_number = account_number
            #movement.ssvscs = something # find out WTF this line "SS/VS/CS" line is
            movement.transaction_type = transaction_type

    def parse_fourth_line(self, statement, movement, line):
        movement.counterparty_details = line.strip()
