"""
Inititalization details for the nextbus_client package
"""
from . import agency
from . import route
from . import route_config
from . import predictions
from . import errors
from .version import __version__
from .client import Client

__title__ = 'nextbus_client'
__author__ = 'Adam Duston'
__email__ = 'compybara@protonmail.com'
__license__ = 'BSD-3-Clause'

__all__ = ['agency', 'route', 'predictions', 'errors', 'client']
