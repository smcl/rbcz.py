from decimal import *
from datetime import datetime

money_regex = r"-?[0-9 ]+\.\d\d"

def to_decimal(s):
    return Decimal(s.replace(" ",""))

def to_long_date(s):
    return datetime.strptime(s, "%d.%m.%Y")

def to_short_date(s, year):
    return to_long_date(s + "." + str(year))
