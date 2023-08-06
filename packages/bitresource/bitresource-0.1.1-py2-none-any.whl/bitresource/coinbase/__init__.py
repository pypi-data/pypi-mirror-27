from http_resource import HttpResource


class CoinbaseHttpResource(HttpResource):
    endpoint_url = 'https://coinbase.com/api/v1/'


ExchangeRates = CoinbaseHttpResource('currencies', 'exchange_rates')
