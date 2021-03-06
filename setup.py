from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(name='gyparody',
      version=version,
      description="Gyparody a game to play with friends.",
      long_description="""\
Gyparody is a game to play with friends and an audience.""",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords='gyparody game-show',
      author='Brandon Edens',
      author_email='brandon@as220.org',
      url='http://brandonedens.org/git/gyparody.git/',
      license='GPL3',
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
