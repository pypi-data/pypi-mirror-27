from ._version import get_versions
VERSION = get_versions()['version']
del get_versions
import sys


PYVERSION = 2
if sys.version_info > (3,):
    PYVERSION = 3


PVERSION = 3
