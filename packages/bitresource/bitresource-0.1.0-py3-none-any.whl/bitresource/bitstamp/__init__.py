from bitresource import registry
from http_resource import HttpResource


@registry.register()
class BitStampResource(HttpResource):
    name = 'bitstamp'
    endpoint_url = 'https://www.bitstamp.net/api/'


ExchangeRates = BitStampResource('ticker')
