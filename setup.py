from setuptools import setup, find_packages
import sys


if sys.version_info.major != 3:
    print('This Python is only compatible with Python 3, but you are running '
          'Python {}. The installation will likely fail.'.format(sys.version_info.major))


setup(name='autograde',
      packages=[package for package in find_packages()
                if package.startswith('autograde')],
      install_requires=[
          'scons'
      ],
      extras_require={
        
      },
      description='A library whose purpose is to help with grading.',
      author='Adolfo Gonzalez III',
      url='',
      author_email='',
      keywords="",
      license="",
      )


