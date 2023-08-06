from bitresource import resource_registry
from http_resource import HttpResource


@resource_registry.register()
class KrakenHttpResource(HttpResource):
    name = 'kraken'
    endpoint_url = 'https://api.kraken.com/0/public/'


CurrencyResource = KrakenHttpResource('Assets')

MarketResource = KrakenHttpResource('AssetPairs')
