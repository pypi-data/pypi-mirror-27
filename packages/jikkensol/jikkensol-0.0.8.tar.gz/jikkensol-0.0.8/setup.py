from setuptools import setup, find_packages
import sys, os

version = '0.0.8'

setup(name='jikkensol',
      version=version,
      description="jikken package",
      long_description="""\
jikken package""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='jikken package',
      author='solima',
      author_email='',
      url='http://www.solima.net/',
      license='GPL',
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
