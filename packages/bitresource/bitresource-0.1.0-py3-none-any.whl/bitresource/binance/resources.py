from bitresource import resource_registry
from dictutils import AttrDict
from http_resource import HttpResource


@resource_registry.register()
class BinanceResource(HttpResource):
    name = 'binance'
    endpoint_url = 'https://www.binance.com/api'

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
            elif 'symbols' in results:
                result_data = results.get('symbols')
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


CurrencyResource = BinanceResource('v1', 'exchangeInfo')

MarketResource = BinanceResource('v1', 'exchangeInfo')

TickerResource = BinanceResource('v3', 'ticker/price')
