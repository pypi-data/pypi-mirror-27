"""
Clash Royale wrapper for cr-api.com
"""
__version__ = "1.0"

from .client import Client
from .client_async import AsyncClient
from .exceptions import APITimeoutError, APIClientResponseError, APIError
from .url import APIURL
from .models import Clan, TopClans, TopPlayers, Tag