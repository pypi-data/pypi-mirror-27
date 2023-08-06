from bitresource import resource_registry
from http_resource import HttpResource


@resource_registry.register()
class CoindeskHttpResource(HttpResource):
    name = 'coindesk'
    endpoint_url = 'https://api.coindesk.com/v1/bpi/'


CurrencyResource = CoindeskHttpResource('supported-currencies.json')


