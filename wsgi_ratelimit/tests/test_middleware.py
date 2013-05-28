
import unittest

from webtest import TestApp
from mock import patch


from wsgi_ratelimit import ratelimit_middleware, WSGI_ENVIRON_PROPERTY


class FakeMemcacheClient:

    paths_filtered = [
        ("GET", "/ok/"),
        ("GET", "/ok/?key"),
        ("GET", "/ok/?key"),
        ("GET", "/ok/?key=id&name=24"),
        ("GET", "/ok/?key=id&name=24&secondname=%27yourname%27"),
        ("POST", "/ok/"),
        ("POST", "/ok/?key=id"),
        ("POST", "/ok/?key=id"),
        ("POST", "/ok/?key=id"),
        ("POST", "/ok/?key=id&name=24"),
        ("POST", "/ok/?key=id&name=24&secondname=%27yourname%27"),
    ]

    paths_not_filtered = [
        ("GET", "/ok"),
        ("GET", "/not/"),
        ("GET", "/"),
        ("POST", "/ok"),
        ("POST", "/not/"),
        ("POST", "/"),
    ]

    original_values = {
        "rt_GET_/ok/_10.0.0.1": 5,
        "rt_POST_/ok/_10.0.0.1": 5,
    }

    def __init__(self, *args, **kwargs):
        self.values = self.original_values

    def get(self, key, **kwargs):
        return self.values.get(key, None)

    def set(self, key, value, **kwargs):
        self.values[key] = value
        return self.values[key]

    def incr(self, key, value=1, **kwargs):
        self.values[key] += value
        return self.values[key]


class FakeWsgiApp:
    """A very simple app wsgi that return:
        True If environ contain WSGI_ENVIRON_PROPERTY
        else False
    """
    def __call__(self, environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        body = str(environ.get(WSGI_ENVIRON_PROPERTY, False))
        response = "{0}\n".format(body)
        return [response]


class RateLimitMiddlewareAppTests(unittest.TestCase):

    def setUp(self):
        settings = {
            'memcached.hosts': '127.0.0.1:11211',
            'memcached.prefix': 'rt',
            'expire_time': '60',
            'max_rate': '5',
            'protected_paths': '\nGET /ok/\nPOST /ok/\n',
        }

        with patch("memcache.Client", FakeMemcacheClient):
            app = ratelimit_middleware({}, **settings)
            app = app(FakeWsgiApp())

            self.testapp1 = TestApp(app, extra_environ={"REMOTE_ADDRESS": "10.0.0.1"})
            self.testapp2 = TestApp(app, extra_environ={"REMOTE_ADDRESS": "10.0.0.2"})

    def _request_test(self, func, path):
        response = func(path)
        return response.body.startswith("True")

    def test_notfiltered_request(self):
        for (method, query) in FakeMemcacheClient.paths_not_filtered:
            if method == "GET":
                func = self.testapp1.get
            else:
                func = self.testapp1.post
            self.assertFalse(self._request_test(func, query))

    def test_filtered_ratelimit_request(self):
        for (method, query) in FakeMemcacheClient.paths_filtered:
            if method == "GET":
                func = self.testapp1.get
            else:
                func = self.testapp1.post
            self.assertTrue(self._request_test(func, query))

        for pet in range(1, 8):
            if pet <= 5:
                self.assertFalse(self._request_test(self.testapp2.get, "/ok/"))
            else:
                self.assertTrue(self._request_test(self.testapp2.get, "/ok/"))
