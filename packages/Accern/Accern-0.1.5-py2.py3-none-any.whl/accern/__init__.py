"""Accern: python library for Accern API.

Accern is a python library to query, download, filter and save Accern Data.
"""

from accern.api import API
from accern.historical import HistoricalClient
from accern.stream import StreamClient, StreamListener
from accern.default_client import AccernClient

token = None


__all__ = [
    'API',
    'AccernClient',
    'HistoricalClient',
    'StreamClient',
    'StreamListener'
]
