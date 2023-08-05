"""
Endpoints

Simply keeps all API enpoint URIs organized and out of the major logic
"""


__all__ = ('API_URL', 'CANDLES_PATH', 'CURRENCIES_PATH', 'ORDERS_PATH',
           'PRODUCTS_PATH', 'STATS_PATH', 'TICKER_PATH', 'TIME_PATH',
           'TRADES_PATH')

API_URL = 'https://api.gdax.com'

# Public endpoints
CANDLES_PATH = '/products/{product_id}/candles'
CURRENCIES_PATH = '/currencies'
ORDERS_PATH = '/products/{product_id}/book'
PRODUCTS_PATH = '/products'
STATS_PATH = '/products/{product_id}/stats'
TICKER_PATH = '/products/{product_id}/ticker'
TIME_PATH = '/time'
TRADES_PATH = '/products/{product_id}/trades'
