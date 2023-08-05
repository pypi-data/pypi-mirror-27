"""
Public Client

Defines a wrapper for the public API endpoint
"""
from datetime import timedelta

import requests

from gdax.endpoints import *
from gdax.exceptions import ExcessivePaginationErrors
from gdax.exceptions import ExcessivePaginationRequests
from gdax.validators import *


__all__ = ('PublicClient',)

DEFAULT_MAX_PAGINATION_ERRORS = 10
DEFAULT_MAX_PAGINATION_REQUESTS = 100
DEFAULT_TIMEOUT = 30 # seconds
MAX_RECORDS_PER_REQUEST = 100
MAX_CANDLES_PER_REQUEST = 200
MIN_GRANULARITY = 30


class PublicClient(object):
    """GDAX public API client

    A wrapper for sending requests to GDAX public API endpoints

    Attributes:
        url (str): The base URL of the API (defaults to GDAX)
        timeout (int): The default timeout in seconds for HTTP requests
        validate_args (bool): Switch to enable validation of method parameters
            (defaults to False)
        max_pagination_errors (int): Maximum number of pagination errors
            allowed before aborting a paginated request (defaults to 10)
        max_pagination_requests (int): Maximum number of pagination
            requests allowed for a single method call before aborting a
            paginated request (defaults to 100)
    """


    def __init__(self, api_url=API_URL,
                 timeout=DEFAULT_TIMEOUT,
                 validate_args=False,
                 max_pagination_errors=DEFAULT_MAX_PAGINATION_ERRORS,
                 max_pagination_requests=DEFAULT_MAX_PAGINATION_REQUESTS):
        """Initialize a PublicClient instance

        Args:
            api_url (str, optional): The base URL of the API (defaults to
               GDAX)
            timeout (int, optional): The default timeout value in seconds
                for HTTP requests
            validate_args (bool, optional): Switch to enable validation of
                method parameters (defaults to False)
            max_pagination_errors (int, optional): Maximum number of
                pagination errors allowed before aborting a paginated request
                (defaults to 10)
            max_pagination_requests (int, optional): Maximum number of
                pagination requests allowed for a single method call before
                aborting a paginated request (defaults to 100)

        Returns:
            An instantiated PublicClient object
        """
        if validate_args:
            assert isinstance(api_url, str)
            assert len(api_url) > 0
            assert isinstance(timeout, int)
            assert timeout > 0
            assert isinstance(max_pagination_errors, int)
            assert max_pagination_errors > 0
            assert isinstance(max_pagination_requests, int)
            assert max_pagination_requests > 0

        self.url = api_url.rstrip('/')
        self.timeout = timeout
        self.validate_args = validate_args
        self.max_pagination_errors = max_pagination_errors
        self.max_pagination_requests = max_pagination_requests


    def _get(self, endpoint_url, params=None, timeout=None):
        if not timeout:
            timeout = self.timeout

        r = requests.get(endpoint_url, params=params, timeout=timeout)
        return r.json()


    def get_candles_for_product(self, product_id, start, end, granularity=900,
                                endpoint_path=CANDLES_PATH,
                                timeout=None):
        """Get candles for a product

        Args:
            product_id (str): The product ID (e.g., 'BTC-USD')
            start (datetime): The starting date of the request window
            end (datetime): The ending date of the request window
            granularity (int, optional): The candle granularity in seconds
            endpoint_path (str, optional): The path to the endpoint (excluding
                the URL)
            timeout (int, optional): Request timeout in seconds

        Returns:
            list of candle descriptions
        """
        if not timeout:
            timeout = self.timeout

        if self.validate_args:
            validate_endpoint_path_and_timeout(endpoint_path, timeout)
            validate_start_and_end(start, end)
            validate_granularity(granularity)

        page_start = start
        page_length = timedelta(
            seconds=granularity*MAX_CANDLES_PER_REQUEST)
        page_end = page_start + page_length
        if page_end > end:
            page_end = end

        data = []
        error_counter = 0
        loop_counter = 0
        while page_start < end:
            params = {
                'start': page_start.isoformat(),
                'end': page_end.isoformat(),
                'granularity': granularity,
            }

            r = requests.get(
                    self.url + endpoint_path.format(product_id=product_id),
                    params=params,
                    timeout=timeout)

            if r.status_code == 200:
                data.extend(r.json())
                page_start = page_end
                page_end = page_start + page_length

                if page_end > end:
                    page_end = end

            else:
                error_counter = error_counter + 1

            if error_counter >= self.max_pagination_errors:
                raise ExcessivePaginationErrors(
                    'Reached pagination error limit {}'.format(error_counter))

            if loop_counter >= self.max_pagination_requests:
                raise ExcessivePaginationRequests(
                    'Reached paginations request limit {}'.format(
                        loop_counter))

            loop_counter = loop_counter + 1

        return data


    def get_currencies(self, endpoint_path=CURRENCIES_PATH, timeout=None):
        """Get the list of current currencies (e.g., BTC)

        Args:
            endpoint_path (str, optional): The path to the endpoint
                (excluding the URL)
            timeout (int, optional): Request timeout in seconds

        Returns:
            list of currency descriptions
        """
        if not timeout:
            timeout = self.timeout

        if self.validate_args:
            validate_endpoint_path_and_timeout(endpoint_path, timeout)

        return self._get(self.url+endpoint_path, timeout=timeout)


    def get_orders_for_product(self, product_id, level=1,
                               endpoint_path=ORDERS_PATH,
                               timeout=None):
        """Get the current order book for a product

        Args:
            product_id (str): The product ID (e.g., 'BTC-USD')
            level (int, optional): The order book detail level (1, 2, or 3)
            endpoint_path (str, optional): The path to the endpoint (excluding
                the URL)
            timeout (int, optional): Request timeout in seconds

        Returns:
            list of order descriptions
        """
        if not timeout:
            timeout = self.timeout

        if self.validate_args:
            validate_endpoint_path_and_timeout(endpoint_path, timeout)
            validate_product_id(product_id)
            assert level in (1, 2, 3)

        return self._get(self.url+endpoint_path.format(product_id=product_id),
                         params={'level':level},
                         timeout=timeout)


    def get_products(self, endpoint_path=PRODUCTS_PATH, timeout=None):
        """Get the list of current products (e.g., BTC-USD)

        Args:
            endpoint_path (str, optional): The path to the endpoint
                (excluding the URL)
            timeout (int, optional): Request timeout in seconds

        Returns:
            list of product descriptions
        """
        if not timeout:
            timeout = self.timeout

        if self.validate_args:
            validate_endpoint_path_and_timeout(endpoint_path, timeout)

        return self._get(self.url + endpoint_path, timeout=timeout)


    def get_stats_for_product(self, product_id, endpoint_path=STATS_PATH,
                              timeout=None):
        """Get 24hr statistics for a product

        Args:
            product_id (str): The product ID (e.g., 'BTC-USD')
            endpoint_path (str, optional): The path to the endpoint (excluding
                the URL)
            timeout (int, optional): Request timeout in seconds

        Returns:
            dict with statistics
        """
        if not timeout:
            timeout = self.timeout

        if self.validate_args:
            validate_endpoint_path_and_timeout(endpoint_path, timeout)
            validate_product_id(product_id)

        return self._get(self.url+endpoint_path.format(product_id=product_id),
                         timeout=timeout)


    def get_ticker_for_product(self, product_id, endpoint_path=TICKER_PATH,
                               timeout=None):
        """Get the latest ticker for a product

        Args:
            product_id (str): The product ID (e.g., 'BTC-USD')
            endpoint_path (str, optional): The path to the endpoint (excluding
                the URL)
            timeout (int, optional): Request timeout in seconds

        Returns:
            dict with ticker information
        """
        if not timeout:
            timeout = self.timeout

        if self.validate_args:
            validate_endpoint_path_and_timeout(endpoint_path, timeout)
            validate_product_id(product_id)

        return self._get(self.url+endpoint_path.format(product_id=product_id),
                         timeout=timeout)


    def get_time(self, endpoint_path=TIME_PATH, timeout=None):
        """Get server time

        Args:
            endpoint_path (str, optional): The path to the endpoint (excluding
                the URL)
            timeout (int, optional): Request timeout in seconds

        Returns:
            dict with time description
        """
        if not timeout:
            timeout = self.timeout

        if self.validate_args:
            validate_endpoint_path_and_timeout(endpoint_path, timeout)

        return self._get(self.url+endpoint_path, timeout=timeout)


    def get_trades_for_product(self, product_id, after=None, before=None,
                               limit=MAX_RECORDS_PER_REQUEST,
                               endpoint_path=TRADES_PATH,
                               timeout=None,
                               return_paging_headers=False):
        """Get trades for a product

        Args:
            product_id (str): The product ID (e.g., 'BTC-USD')
            after (int, optional): Return records after this trade ID
            before (int, optional): Return records before this trade ID
            limit (int, optional): Number of records to return
            endpoint_path (str, optional): The path to the endpoint (excluding
                the URL)
            timeout (int, optional): Request timeout in seconds
            return_paging_headers (bool, optional): If true, method will
                return a tuple with (data, after, before)

        Returns:
            list with trade descriptions if return_paging_headers is False
            tuple with (data, after, before) if return_paging_headers is True
        """
        if not timeout:
            timeout = self.timeout

        if self.validate_args:
            validate_endpoint_path_and_timeout(endpoint_path, timeout)
            validate_product_id(product_id)
            validate_after_and_before(after, before)
            validate_limit(limit)

        page_limit = limit
        if limit > MAX_RECORDS_PER_REQUEST:
            page_limit = MAX_RECORDS_PER_REQUEST

        data = []
        error_counter = 0
        loop_counter = 0
        while len(data) < limit:
            url = self.url \
                  + endpoint_path.format(product_id=product_id) \
                  + '?limit={}'.format(page_limit)

            if after:
                url = url + '&after={}'.format(after)

            if before:
                url = url + '&before={}'.format(before)

            r = requests.get(url, timeout=timeout)

            if r.status_code == 200:
                data.extend(r.json())
                after = r.headers['CB-AFTER']
                before = r.headers['CB-BEFORE']

            else:
                error_counter = error_counter + 1

            if error_counter >= self.max_pagination_errors:
                raise ExcessivePaginationErrors(
                    'Reached pagination error limit {}'.format(error_counter))

            if loop_counter >= self.max_pagination_requests:
                raise ExcessivePaginationRequests(
                    'Reached paginations request limit {}'.format(
                        loop_counter))

            loop_counter = loop_counter + 1

        if return_paging_headers:
            return (data, before, after)

        return data