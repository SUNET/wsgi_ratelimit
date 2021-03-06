import re

import memcache


PROTECTED_PATHS_RE = re.compile(r"^(POST|GET|PUT|UPDATE)(?: *)(.*)$")

__all__ = [
    "RateLimitMiddleware",
    "ratelimit_middleware",
    "is_ratelimit_reached",
    "WSGI_ENVIRON_PROPERTY",
]

WSGI_ENVIRON_PROPERTY = "RATELIMIT_REACHED"


def is_ratelimit_reached(environ):
    if isinstance(environ, dict):
        return environ.get(WSGI_ENVIRON_PROPERTY, False)
    return False


class RateLimitMiddleware:

    def __init__(self, application, cache, prefix,
                 protected_paths, expire_time, max_rate):

        self.application = application
        self.cache = cache
        self.prefix = prefix
        self.protected_paths = protected_paths
        self.expire_time = expire_time
        self.max_rate = max_rate

    def __call__(self, environ, start_response):

        if self.is_request_protected(environ) and self.new_request(environ):
            environ[WSGI_ENVIRON_PROPERTY] = True

        return self.application(environ, start_response)

    def is_request_protected(self, environ):
        request = (environ.get("REQUEST_METHOD"), environ.get("PATH_INFO"), )
        return request in self.protected_paths

    def generate_request_key(self, environ):
        return "{0}_{1}_{2}_{3}".format(self.prefix,
                                        environ.get("REQUEST_METHOD"),
                                        environ.get("PATH_INFO"),
                                        environ.get("REMOTE_ADDRESS"))

    def new_request(self, environ):
        key = self.generate_request_key(environ)
        if self.cache.get(key) is None:
            self.cache.set(key, 0, time=self.expire_time)
        rate = self.cache.incr(key)
        return rate > self.max_rate


def ratelimit_middleware(global_config, **settings):

    memcached_hosts = settings.get('memcached.hosts', '127.0.0.1:11211')
    prefix = settings.get('memcached.prefix', 'rt')

    expire_time = int(settings.get('expire_time', '60'))
    max_rate = int(settings.get('max_rate', '60'))

    protected_paths_set = settings.get('protected_paths', '')

    protected_paths = []
    for line in protected_paths_set.split("\n"):
        ppath = PROTECTED_PATHS_RE.search(line)
        if ppath and ppath.groups():
            protected_paths.append(ppath.groups())

    if '\n' in memcached_hosts:
        memcached_uri = memcached_hosts.split("\n")
    elif ';' in memcached_hosts:
        memcached_uri = memcached_hosts.split(";")
    else:
        memcached_uri = [memcached_hosts]

    cache = memcache.Client(memcached_uri, debug=0)

    def factory(app, *args, **kwargs):
        return RateLimitMiddleware(app, cache, prefix, protected_paths,
                                   expire_time, max_rate)

    return factory
