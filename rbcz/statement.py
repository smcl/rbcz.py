class Statment(object):
    def __init__(self):
        self.account_name = ""
        self.account_number = ""
        self.iban = ""
        self.currency = ""
        self.number = -1
        self.from_date = None
        self.to_date = None
        self.opening_balance = 0
        self.income = 0
        self.expenses = 0
        self.closing_balance = 0
        self.blocked = 0
        self.receivable = 0
        self.available_balance = 0
        self.movements = []
    
