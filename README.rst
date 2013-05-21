wsgi_ratelimit
==============

wsgi_ratelimit is a wsgi middleware. It uses memcached to store the amount of
access from the combination of remote_ip, path, http_method. If the counter is
bigger than the allowed rate, then a wsgi environment variable is set,
RATELIMIT_REACHED.  Then, the following app in the WSGI pipeline, like Pyramid
or Repoze.bfg can use it to show a captcha or to return anything else.


Paster/Waitress configuration example
-------------------------------------

This is a example block of paster ini profile configuration:


.. code::

   [app:yourapp]
   use = egg:yourapp
   ...

   [filter:ratelimit]
   use = egg:wsgi_ratelimit

   memcached.hosts = 127.0.0.1:11211
   memcached.prefix = rt

   expire_time = 60
   max_rate = 5

   protected_paths =
       GET /

   [pipeline:main]
   pipeline =
       ratelimit
       yourapp

   [server:main]
   use = egg:waitress#main
   host = 0.0.0.0
   port = 6543


Settings property detailed documentation
----------------------------------------

* **memcached.hosts**: You can add one or more than one servers, one per line
  or *;* separated.

  .. code::

     memcached.hosts = 127.0.0.1:11211

     memcached.hosts = 127.0.0.1:11211;127.0.0.1:11212

     memcached.hosts = 127.0.0.1:11211
                       127.0.0.1:11212


* **memcached.prefix:** This is the key prefix for every key stored in memcached
  by this module. The default value is *rt*

  .. code::

     memcached.prefix = rt

* **expire_time:** This is the time in seconds from the first access. This use
  memcached time expiration key. So after expire_time seconds from the first
  request, the RATELIMIT_REACHED was not set because the counter is reset to
  zero. The default value is 60:

  .. code::

     expire_time = 60

* **max_rate:** When a user do more requests than *max_rate* in the time set in
  *expire_time*, the RATELIMIT_REACHED wsgi environment variable is set. The
  default valu is 60:

  .. code::

     max_rate = 60

* **protected_paths:** This property has the combination of *request_method*
  and *path* that will be protected. You can add more than one separated by
  lines.

  .. code::

     protected_paths =
         GET /
         GET /api/stats/
         POST /api/register/


