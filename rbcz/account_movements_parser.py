import re
from datetime import datetime
from .movement import Movement
from .utils import (
    to_decimal,
    money_regex
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
                #for line in movement:
                self.parse_first_line(m, movement[0])
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
    
    def parse_first_line(self, movement, line):
        first_regex = r"\s*(\d+)\s+(\d\d\.\d\d)\.(.*)(\d\d\.\d\d)\.\s{5}\d?\s+(%s)" % (money_regex)

        first_match = re.match(first_regex, line)

        if first_match:
            movement.number = first_match.group(1)
            movement.date = first_match.group(4)
            movement.amount = to_decimal(first_match.group(5))
            
