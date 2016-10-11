# rbcz.py
Python library for interacting with Raiffeisen Bank's bank statements, which are plaintext files that you should receive every month to your primary email address.

Note: currently *doesn't work* - I started working on this properly today, only the rough structure of the code to get things straight in my head.

## using

```
from rbcz import *
stmt = rbcz.read_statement("16008_6986230001_CZK.TXT")

print "number: " + stmt.number
print "account name: " + stmt.account_name
print "account number: " + stmt.account_number
print "from: " + stmt.from_date
print "to: " + stmt.to_date
print "iban: " + stmt.iban
print "currency: " + stmt.currency
print "opening balance: " + stmt.opening_balance
print "closing balance: " + stmt.closing_balance
print "expenses: " + stmt.expenses
print "income: " + stmt.income
```

## ideas

Should be able to load
- individual statement
- collection of statements
- statements from IMAP connection

My statements are in English, but get hold of Czech ones to see if we can handle both.

Once it's roughly working chuck together a simple example to read in a chunk of statements and plot balance over time in `matplotlib`
