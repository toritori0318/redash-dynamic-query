import unittest

class TestImport(unittest.TestCase):
    def test_import(self):
        from redash_dynamic_query import RedashDynamicQuery
        a = RedashDynamicQuery('','','')
        assert True
