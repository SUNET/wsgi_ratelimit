import unittest

from wsgi_ratelimit import RateLimitMiddleware

"""
Test the basics of WSGI ratelimit.
"""

# only one test case so far, to get this through the CI ;)

class TestBasics(unittest.TestCase):

    def setUp(self):
        cache = {}
        prefix = 'prefix'
        protected_paths = [('GET', '/private',)]
        expire_time = 90
        max_rate = 5
        self.rlimit = RateLimitMiddleware('testapp', cache, prefix,
                                          protected_paths,
                                          expire_time, max_rate)

    def test_is_protected(self):
        self.assertTrue(self.rlimit.is_request_protected(
                {'REQUEST_METHOD': 'GET',
                 'PATH_INFO': '/private',
                 }))
        self.assertFalse(self.rlimit.is_request_protected(
                {'REQUEST_METHOD': 'HEAD',
                 'PATH_INFO': '/private',
                 }))
        self.assertFalse(self.rlimit.is_request_protected(
                {'REQUEST_METHOD': 'GET',
                 'PATH_INFO': '/public',
                 }))
