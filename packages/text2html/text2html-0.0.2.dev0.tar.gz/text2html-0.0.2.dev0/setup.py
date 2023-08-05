from setuptools import setup, find_packages
import sys, os

version = '0.0.2'

setup(name='text2html',
      version=version,
      description="create HTML files from some text files",
      long_description="""\
create HTML files from some text files""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='HTML text file create',
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
      sohtml = text2html.sohtml:main
      """,
      )
