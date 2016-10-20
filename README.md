# rbcz.py [![Build Status](https://api.travis-ci.org/smcl/rbcz.py.svg?branch=master)](https://travis-ci.org/smcl/rbcz.py) [![Coverage Status](https://coveralls.io/repos/github/smcl/rbcz.py/badge.svg)](https://coveralls.io/github/smcl/rbcz.py?branch=master)


`rbcz` is a Python library for parsing the bank statements that Raiffeisen Bank send out via email. It exposes a simple API to either parse statements stored locally or to retrieve them from your IMAP server.

## Methods

There are three simple functions which `read_statement`, `read_statements` and `read_statements_from_imap`. To parse a single statement saved we can use the `read_statement` function, which takes a single parameter - the path to the bank statement on the local filesystem - and returns a `Statement` object:

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

If we don't have all our statements stored locally we can use `read_statements_from_imap` to connect to an IMAP server and search it for emails from the "info@rb.cz" address, download and parse the attachments and return a list of `Statement`.

```
from rbcz import *

statements = read_statements_from_imap("imap.gmail.com", "my.email.address@gmail.com", "password123", "inbox")
```

## Types

There are two types - `Statement` and `Movement`. 

### Statement

A `Statement` represents a monthly statement:

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

### Movement

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

The following script will attempt to parse all the files in the `./rb` directory, then take the closing balance and high/low water marks of each period and plot it on a graph.

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

# load and sort the statements
statements = sorted(
    rbcz.read_statements([ "./tmp/" + f for f in os.listdir("./tmp") ]),
    key=lambda stmt: stmt.from_date)

# function to deterine high/low-water mark on account
def high_low_water(stmt):
    bal = stmt.opening_balance
    hwm = bal
    lwm = bal
    for m in stmt.movements:
        bal += m.amount
        if bal > hwm:
            hwm = bal
        if bal < lwm:
            lwm = bal
    return (lwm, hwm)

#plt.gca().set_color_cycle(['green', 'black', 'red'])


# extract high/low-water marks
water_marks = [ high_low_water(s) for s in statements ]
low_water_marks = [ wm[0] for wm in water_marks ]
high_water_marks = [ wm[1] for wm in water_marks ]

# extract closing balance and dates
closing_balances = [ s.closing_balance for s in statements ]
dates = date2num([ s.from_date for s in statements ])

# prepare and display the chart using matplotlib
y = arange(len(dates)*1.0)

# plot the data
fig, ax = plt.subplots()
ax.set_color_cycle(['green', 'black', 'red'])
ax.plot_date(dates, high_water_marks, "o-")
ax.plot_date(dates, closing_balances, "o-")
ax.plot_date(dates, low_water_marks, "o-")

# fix up the axes
ax.xaxis.set_major_locator(YearLocator())
ax.xaxis.set_minor_locator(MonthLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

ax.fmt_xdata = DateFormatter('%Y-%m-%d')
fig.autofmt_xdate()

# add a legend
ax.legend(['highest', 'closing', 'lowest'], loc='upper left')

plt.show()
```

This will generate a graph like the following:

![rbcz.png](rbcz.png?raw=true)

# TODO

* get coverage to 100%
* fix up IMAP support (it's untested and probably fucked)
* check if it's possible to improve the parsing - there are a LOT of regexes that I throw around and it's not pretty...
* ssvsvc is actually three fields - ss/vs/vc. confirm what they are, split them out and make sure they're parsed and stored
* check if anyone I know gets Czech statements, see if we can parse them too. Is there any other languages - German?
* check if it works for non-Czech-Republic Raiffeisen
