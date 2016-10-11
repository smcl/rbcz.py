def read_statement(filename):
    """
    something like...

    with f as open(filename):
        return StatementParser.parse(f)
    """
    
    pass

def read_statements(filenames):
    """
    something like...

    statements = []

    for filename in filenames:
        statements.append(read_statement(filename))

    return statements
    """

    pass

def read_statements_from_mailbox(imap_addr, username, password, mailbox="inbox"):
    """
    from https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
    something like...

    import imaplib
    
    M = imaplib.IMAP4()
    M.login(getpass.getuser(), getpass.getpass())
    M.select()
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        print 'Message %s\n%s\n' % (num, data[0][1])
    M.close()
    M.logout()

    """
    pass
    
    
