import unittest

from wsgi_ratelimit import is_ratelimit_reached, WSGI_ENVIRON_PROPERTY


class IsRatelimitReachedTests(unittest.TestCase):

    def test_is_ratelimit_reached(self):
        environ = {
            WSGI_ENVIRON_PROPERTY: True
        }
        self.assertTrue(is_ratelimit_reached(environ))

    def test_isnot_ratelimit_reached(self):

        environ = {}
        self.assertFalse(is_ratelimit_reached(environ))

        environ = {
            WSGI_ENVIRON_PROPERTY: False
        }
        self.assertFalse(is_ratelimit_reached(environ))
