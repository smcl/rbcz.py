from email import message_from_string
from imaplib import IMAP4_SSL
from .statement_parser import StatementParser


def read_statement(filename):
    with open(filename) as f:
        return StatementParser().Parse(f.readlines())


def read_statements(filenames):
    return [read_statement(filename) for filename in filenames]


def read_statements_from_imap(hostname, username, password, mailbox="inbox"):
    m = IMAP4_SSL(hostname)
    m.login(username, password)

    m.select(mailbox)
    status, email_ids = m.search(None, '(FROM "info@rb.cz")')

    statements = []

    for num in email_ids[0].split():
        try:
            typ, data = m.fetch(num, '(RFC822)')
            text = data[0][1]
            msg = message_from_string(text)
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                data = part.get_payload(decode=True)
                if not data:
                    continue
                statements.append(StatementParser().Parse(data.split("\n")))
        except:
            # in future add an option to except/print on error
            # for now just eat it and move on
            pass

    m.close()
    m.logout()

    return statements
