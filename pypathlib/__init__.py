# -*- coding: utf-8 -*-
#
from __future__ import print_function

from .__about__ import __author__, __email__, __license__, __version__, __status__

from .path import Path
from .closed_path import ClosedPath

__all__ = [
    "__author__",
    "__email__",
    "__license__",
    "__version__",
    "__status__",
    "ClosedPath",
    "Path",
]

# try:
#     import pipdate
# except ImportError:
#     pass
# else:
#     if pipdate.needs_checking(__name__):
#         print(pipdate.check(__name__, __version__), end="")
