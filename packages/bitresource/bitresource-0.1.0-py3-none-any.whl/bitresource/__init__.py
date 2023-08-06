from bitutils.objects import Exchange
from registry import Registry


class ResourceRegistry(Registry):
    def get_object_name(self, data):
        if hasattr(data, 'name'):
            exchange_name = getattr(data, 'name')

            exchange_registry.register(Exchange(name=exchange_name), name=exchange_name)

            return exchange_name

        return super(ResourceRegistry, self).get_object_name(data)


exchange_registry = Registry()
currency_registry = Registry()
market_registry = Registry()
resource_registry = ResourceRegistry()

# from bitresource import bitpay
# from bitresource import bitstamp
from bitresource import bittrex
from bitresource import binance
from bitresource import blockchain
# from bitresource import coinbase
from bitresource import coindesk
# from bitresource import kraken
