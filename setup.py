from setuptools import setup, find_packages

version = '0.1'


requires = [
    "python-memcached"
],

testing_requires = [
    'WebTest',
    'mock'
]

testing_extras = testing_requires + [
    'nose==1.2.1',
    'coverage==3.6',
]

setup(name='wsgi_ratelimit',
      version=version,
      description="Request rate limit over WSGI",
      long_description="""
wsgi_ratelimit is a wsgi middleware. It uses memcached to store the amount of
access from the combination of remote_ip, path, http_method. If the counter is
bigger than the allowed rate, then a wsgi environment variable is set,
RATELIMIT_REACHED.  Then, the following app in the WSGI pipeline, like Pyramid
or Repoze.bfg can use it to show a captcha or to return anything else.
      """,
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='wsgi',
      author='NORDUnet A/S',
      author_email='',
      url='https://github.com/SUNET/wsgi_ratelimit',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=testing_requires,
      extras_require={
          "testing": testing_extras,
      },
      entry_points="""
      # -*- Entry points: -*-
      [paste.filter_factory]
      main = wsgi_ratelimit:ratelimit_middleware
      """,
      )
