# set the version of the application
__version__ = '0.2.0'

# setup whether logging will be verbose
from os import environ
from distutils.util import strtobool
VERBOSE = bool(strtobool(environ.get('VERBOSE', 'false')))
