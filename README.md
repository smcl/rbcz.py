# rbcz.py
Python library for interacting with Raiffeisen Bank's bank statements, which are plaintext files that you should receive every month to your primary email address.

Note: currently *doesn't work* - I started working on this properly today, only the rough structure of the code to get things straight in my head.

## using

```
from rbcz import rbcz
stmt = rbcz.read_statement("16008_6986230001_CZK.TXT")
print(s.available_balance)
```

## ideas

Should be able to load
- individual statement
- collection of statements
- statements from IMAP connection

My statements are in English, but get hold of Czech ones to see if we can handle both.