from bitresource import resource_registry, exchange_registry
from bitutils.objects import Currency, Market, Ticker
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
    def get_currencies(cls):
        results = []

        for currency in CurrencyResource.data():
            currency = Currency(code=currency.Currency, name=currency.CurrencyLong, type=currency.CoinType)
            results.append(currency)

        return results

    @classmethod
    def get_markets(cls):
        results = []

        for market in MarketResource.data():
            base = market.BaseCurrency
            quote = market.MarketCurrency
            market_code = '%s%s' % (base, quote)
            market_name = '%s-%s' % (base, quote)

            market = Market(code=market_code, name=market_name, base=base, quote=quote)
            results.append(market)

        return results

    @classmethod
    def ticker(cls, market, exchange):
        """{'Last': 0.01798739, 'Ask': 0.01798739, 'Bid': 0.017987}"""
        data = TickerResource.data(market=market.name).first()

        return Ticker(bid=data.Bid, ask=data.Ask, last=data.Last, market=market, exchange=exchange)


CurrencyResource = BittrexResource('public', 'getcurrencies')

MarketResource = BittrexResource('public', 'getmarkets')

TickerResource = BittrexResource('public', 'getticker')
