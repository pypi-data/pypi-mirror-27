import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# IPython 6.0+ does not support Python 2.6, 2.7, 3.0, 3.1, or 3.2
if sys.version_info < (3,3):
    ipython = "ipython>=5.1,<6.0"
else:
    ipython = "ipython>=5.1"    
    
setup(
    name='pyrfume',
    version='0.01',
    author='Rick Gerkin',
    author_email='rgerkin@asu.edu',
    packages=['pyrfume'],
    url='http://pyrfume.scidash.org',
    license='MIT',
    description='A valdiation library for human olfactory psychophysics research.',
    install_requires=[],
)



