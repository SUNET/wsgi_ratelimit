from setuptools import setup, find_packages

version = '0.1'


def get_long_description():
    readme = open('README.rst', 'r')
    readme_text = readme.read()
    readme.close()
    return readme_text

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
      long_description=get_long_description(),
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
