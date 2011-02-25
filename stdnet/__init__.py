'''A networked standard template library for Python.'''
VERSION = (0, 5, '1dev')
 
def get_version():
    return '.'.join(map(str,VERSION))
 
__version__ = get_version()
__license__ = "BSD"
__author__ = "Luca Sbardella"
__contact__ = "luca.sbardella@gmail.com"
__homepage__ = "https://github.com/lsbardel/python-stdnet"


sphinxtogithub = True

from .exceptions import *

from .backends import *