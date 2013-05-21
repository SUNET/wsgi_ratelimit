from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='wsgi_ratelimit',
      version=version,
      description="Request rate limit over WSGI",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='wsgi',
      author='NORDUnet A/S',
      author_email='',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
