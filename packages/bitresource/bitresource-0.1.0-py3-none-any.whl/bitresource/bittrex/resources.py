from bitresource import resource_registry
from dictutils import AttrDict
from http_resource import HttpResource


@resource_registry.register()
class BittrexResource(HttpResource):
    name = 'bittrex'
    endpoint_url = 'https://bittrex.com/api/v1.1'

    def results_iter(self, response, **kwargs):
        results = response.json()
        result_data = []

        if type(results) is dict:
            if 'result' in results:
                results = results.get('result')
                if type(results) is dict:
                    yield AttrDict(results)
                else:
                    result_data = results
            else:
                result_data = list(results.items())

        for result in result_data:

            if type(result) is tuple:
                result[1].update({'_key': result[0]})
                yield AttrDict(result[1])
            else:
                yield AttrDict(result)

    @classmethod
    def ticker(cls, market):
        return TickerResource.data(market=market).first()


CurrencyResource = BittrexResource('public', 'getcurrencies')

MarketResource = BittrexResource('public', 'getmarkets')

TickerResource = BittrexResource('public', 'getticker')
