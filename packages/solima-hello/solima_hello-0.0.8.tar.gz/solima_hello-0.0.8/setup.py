from setuptools import setup, find_packages
import sys, os

version = '0.0.8'

setup(name='solima_hello',
      version=version,
      description="solima hello world",
      long_description="""\
solima hello world""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='solima,hello,world',
      author='solima',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      solhello = solima_hello.hello:main
      """,
      )
