import unittest2

# need to ensure that the package exports the following symbols:
#
# - read_statement
# - read_statements
# - read_statements_from_imap


class TestImports(unittest2.TestCase):

    def test_import(self):
        from rbcz import rbcz
        dir_rbcz = dir(rbcz)
        self.assertIn("read_statement", dir_rbcz)
        self.assertIn("read_statements", dir_rbcz)
        self.assertIn("read_statements_from_imap", dir_rbcz)
