import unittest

from redash_dynamic_query import RedashDynamicQuery


class TestRedashDynamicQuery(unittest.TestCase):
    def test_bind_params(self):
        redash = RedashDynamicQuery('', '', '')
        bind = {'user_id': 123}

        self.assertEqual(
            redash._bind_params('SELECT * FROM users;', None),
            'SELECT * FROM users;')
        self.assertEqual(
            redash._bind_params('SELECT * FROM users WHERE id={{user_id}};', bind),
            'SELECT * FROM users WHERE id=123;')
        self.assertEqual(
            redash._bind_params('SELECT * FROM users WHERE id={{ user_id }};', bind),
            'SELECT * FROM users WHERE id=123;')
        self.assertEqual(
            redash._bind_params('SELECT * FROM users WHERE id={{{user_id}}};', bind),
            'SELECT * FROM users WHERE id=123;')
        self.assertEqual(
            redash._bind_params('SELECT id REGEXP \'^[0-9]{1,4}\' FROM users WHERE id={{user_id}};', bind),
            'SELECT id REGEXP \'^[0-9]{1,4}\' FROM users WHERE id=123;')


if __name__ == '__main__':
    unittest.main()
