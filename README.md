# rbcz.py
`rbcz` is a Python library for parsing the bank statements that Raiffeisen Bank send out via email. There are three simple functions which `read_statement`, `read_statements` and `read_statements_from_mailbox`.

## read_statement

To parse a single statement saved we can use the `read_statement` function, which takes a single parameter - the path to the bank statement on the local filesystem:

```
from rbcz import *
statement = rbcz.read_statement("/path/to/stmt_january_czk.txt")
```

This returns a `Statement` object which has the following properties:

* `account_name` - (string) the name of the main account holder (your name!)
* `account_number` - (string) your account number
* `iban` - (string) the IBAN of your account
* `currency` - (string) the currency the account holds
* `number` - (int) the number of the statement (your first statement will be `1`)
* `from_date` - (string) the opening date of the statement
* `to_date` - (string) the closing date of the statement
* `opening_balance` - (Decimal) the balance at the opening date of the statement
* `income` - (Decimal) the income you've received during the statement's reporting period
* `expenses` - (Decimal) the expenses you've paid out during the statement's reporting period
* `closing_balance` - (Decimal) the balance at the closing date of the statement
* `blocked` - (Decimal) amount ringfenced for payments out
* `receivable` - (Decimal) amount received but yet to clear/settle
* `available_balance` - (Decimal) amount of money available to withdraw at the closing date of the statement
* `movements` - (List of Movement) the individual cash movements (payments in or out) during the reporting period

The `movements` property is a list of type `Movement`, each of which has the following properties:
* `number` - (int) id of the movement in this statement
* `amount` - (Decimal) amount of the thing
* `date` - (Date) the date which the payment was created at

## read_statements

Similar to `read_statement` but instead accepts a `List` of filenames and returns a `List` of `Statement`:

```
from rbcz import *

statement_filenames = [
    "stmt_jan_czk.txt",
    "stmt_feb_czk.txt",
    "stmt_mar_czk.txt"
]

statements = rbcz.read_statements(statement_filenames)
```

## read_statements_from_mailbox

Use with caution. Call it with IMAP credentials and it'll log in, search for bank statements, download, parse and return them.

*NOTE: NOT IMPLEMENTED YET*

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

* double-check we definitely return `Decimal` and `Date` where I've said we do
* more information is available from each `Movement`
* add some tests
* implement IMAP functionality
* check if anyone I know gets Czech statements, see if we can parse them too. Is there any other languages - German?
* check if it works for non-Czech-Republic Raiffeisen

Once it's roughly working chuck together a simple example to read in a chunk of statements and plot balance over time in `matplotlib`
