"""Python API for using chain.so."""
import asyncio
import logging

import aiohttp
import async_timeout

_LOGGER = logging.getLogger(__name__)
_BASE_URL = 'https://chain.so/api/v2/'


class ChainSo(object):
    """A class for handling data from chain.so."""

    def __init__(self, network, address, loop, session):
        """Initialize the data retrieval."""
        self._loop = loop
        self._session = session
        self.network = network
        self.address = address
        self.data = {}

    @asyncio.coroutine
    def async_get_data(self):
        url = '{}/{}/{}/{}'.format(
            _BASE_URL, 'get_address_balance', self.network, self.address)

        try:
            with async_timeout.timeout(5, loop=self._loop):
                response = yield from self._session.get(url)

            _LOGGER.debug("Response from chain.so: %s", response.status)
            data = yield from response.json()
            _LOGGER.debug(data)
        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Can not load data from chain.so")

        if data['status'] == 'success':
            self.data = data['data']
