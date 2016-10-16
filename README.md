# rbcz.py
`rbcz` is a Python library for parsing the bank statements that Raiffeisen Bank send out via email. It exposes a simple API to either parse statements stored locally or to retrieve them from your IMAP server.

## Methods

There are three simple functions which `read_statement`, `read_statements` and `read_statements_from_mailbox`. To parse a single statement saved we can use the `read_statement` function, which takes a single parameter - the path to the bank statement on the local filesystem - and returns a `Statement` object:

```
from rbcz import *
statement = rbcz.read_statement("/path/to/stmt_january_czk.txt")
```

If we have a number of statements locally we can use `read_statements` which accepts a list of filenames to parse, and returns a list of `Statement`:

```
from rbcz import *

statement_filenames = [
    "stmt_jan_czk.txt",
    "stmt_feb_czk.txt",
    "stmt_mar_czk.txt"
]

statements = rbcz.read_statements(statement_filenames)
```

If we don't have all our statements stored locally we can use `read_statements_from_mailbox` to connect to an IMAP server and search it for emails from the "info@rb.cz" address, download and parse the attachments and return a list of `Statement`.

```
from rbcz import *

statements = read_statements_from_mailbox("imap.gmail.com", "my.email.address@gmail.com", "password123", "inbox")
```

## Types

There are two types - `Statement` and `Movement`. A `Statement` represents a monthly statement:

* `account_name` - (string) the name of the main account holder (your name!)
* `account_number` - (string) your account number
* `iban` - (string) the IBAN of your account
* `currency` - (string) the currency the account holds
* `number` - (int) the number of the statement (your first statement will be `1`)
* `from_date` - (datetime) the opening date of the statement
* `to_date` - (datetime) the closing date of the statement
* `opening_balance` - (Decimal) the balance at the opening date of the statement
* `income` - (Decimal) the income you've received during the statement's reporting period
* `expenses` - (Decimal) the expenses you've paid out during the statement's reporting period
* `closing_balance` - (Decimal) the balance at the closing date of the statement
* `blocked` - (Decimal) amount ringfenced for payments out
* `receivable` - (Decimal) amount received but yet to clear/settle
* `available_balance` - (Decimal) amount of money available to withdraw at the closing date of the statement
* `movements` - (List of Movement) the individual cash movements (payments in or out) during the reporting period

A `Movement` is an individual transaction - for example an ATM withdrawal or Debit Card payment. Each `Statement` will have a list of `Movement` called `movements` for all the transactions during the reporting period. Each `Movement` has the following:
* `number` - (int) id of the movement in the current statement
* `amount` - (Decimal) amount of the thing
* `date_deducted` - (datetime) the date the transaction was submitted originally
* `date_completed` - (datetime) the date + time the transaction was finalised at
* `counterparty_account_number` - (string) the account the payment was sent to or received from
* `counterparty_details` - (string) information about the account the payment was sent to or received from, if available
* `narrative` - (string) additional information about the transaction
* `transaction_type` - (string) what type of transaction occurred

# Example

The following script will attempt to parse all the files in the `./rb` directory, then take the closing balance of each period and plot it on a graph.

```
#!/usr/bin/python

# system/lib imports
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, drange, date2num
from numpy import arange

# rbcz library
from rbcz import *

statements = sorted(
    rbcz.read_statements([ "./rb/" + f for f in os.listdir("./rb") ]),
        key=lambda stmt: stmt.from_date)

balances = [ s.closing_balance for s in statements ]
dates = date2num([ s.from_date for s in statements ])

y = arange(len(dates)*1.0)

fig, ax = plt.subplots()
ax.plot_date(dates, balances)

ax.xaxis.set_major_locator(YearLocator())
ax.xaxis.set_minor_locator(MonthLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

ax.fmt_xdata = DateFormatter('%Y-%m-%d')
fig.autofmt_xdate()

plt.show()
```

This will generate a graph like the following:

rbcz.png
![rbcz.png](rbcz.png?raw=true)

# TODO

* confirm some of the mystery fields, like ssvsvc
* find a better way to describe the two "date" fields for each transaction
* check if anyone I know gets Czech statements, see if we can parse them too. Is there any other languages - German?
* check if it works for non-Czech-Republic Raiffeisen