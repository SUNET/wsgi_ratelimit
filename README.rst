wsgi_ratelimit
==============

WSGI wsgi_ratelimit middleware use memcached to store the amount of access from
the combination of remote_ip, path, http_method. If the counter is bigger than
the allowed rate, then a wsgi environment variable is set,  RATELIMIT_REACHED.
Then, the following app in the WSGI pipeline, like Pyramid or Repoze.bfg can
use it to show a captcha or to return anything else.
