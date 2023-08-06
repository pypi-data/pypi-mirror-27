from bitresource import resource_registry
from bitutils.objects import Currency, Market, Ticker
from dictutils import AttrDict
from http_resource import HttpResource


@resource_registry.register()
class BinanceResource(HttpResource):
    name = 'binance'
    endpoint_url = 'https://www.binance.com/api'

    def results_iter(self, response, **kwargs):
        resp_json = response.json()
        result_rows = []

        if type(resp_json) is dict:
            if 'symbols' in resp_json:
                result_rows = resp_json.get('symbols')
            else:
                yield AttrDict(resp_json)

        if result_rows:
            for result_row in result_rows:
                yield AttrDict(result_row)

    @classmethod
    def get_currencies(cls):
        """
            {'icebergAllowed': True,
             'baseAssetPrecision': 8,
             'symbol': 'ETHBTC',
             'baseAsset': 'ETH',
             'quoteAsset': 'BTC',
             'status': 'TRADING',
             'quotePrecision': 8}
        """
        results = []

        for currency in CurrencyResource.data():
            currency = Currency(code=currency.quoteAsset, decimals=currency.quotePrecision)
            results.append(currency)

        return results

    @classmethod
    def get_markets(cls):
        """
            {'icebergAllowed': True,
             'baseAssetPrecision': 8,
             'symbol': 'ETHBTC',
             'baseAsset': 'ETH',
             'quoteAsset': 'BTC',
             'status': 'TRADING',
             'quotePrecision': 8}
        """
        results = []

        for market in MarketResource.data():
            market_name = '%s-%s' % (market.quoteAsset, market.baseAsset)

            market = Market(code=market_name.replace('-', ''), name=market_name, base=market.quoteAsset,
                            quote=market.baseAsset)
            results.append(market)

        return results

    @classmethod
    def ticker(cls, market, exchange):
        symbol = ''.join([market.name.split('-')[1], market.name.split('-')[0]])
        data = TickerResource.data(symbol=symbol).first()

        return Ticker(last=data.price, market=market.code, exchange=exchange)


CurrencyResource = BinanceResource('v1', 'exchangeInfo')

MarketResource = BinanceResource('v1', 'exchangeInfo')

TickerResource = BinanceResource('v3', 'ticker/price')
