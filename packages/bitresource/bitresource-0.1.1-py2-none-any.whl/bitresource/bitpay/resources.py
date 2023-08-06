from bitresource import registry
from http_resource import HttpResource


@registry.register()
class BitPayResource(HttpResource):
    name = 'bitpay'
    endpoint_url = 'https://bitpay.com/api/'


CurrenciesResource = BitPayResource('currencies')

ExchangeRates = BitPayResource('rates')


class BitPayCurrency(BaseCurrency):

    def get_data(self, includes=None, excludes=None):
        rates = bitpay.ExchangeRates.all()
        return {'BTC': dict([(r['code'], Decimal(r['rate'])) for r in rates.data])}