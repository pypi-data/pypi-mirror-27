from bitresource import currency_registry, market_registry
from bitutils.objects import Currency, Market
from .resources import CurrencyResource, MarketResource


def get_currencies():
    return list(CurrencyResource.data())


def get_markets():
    return list(MarketResource.data())


def register_currencies():
    for currency in get_currencies():
        currency_code = currency.Currency

        if currency_code not in currency_registry:
            currency_obj = Currency(code=currency.Currency, name=currency.CurrencyLong, type=currency.CoinType)
        else:
            currency_obj = currency_registry[currency_code]

        currency_obj.exchanges.append(CurrencyResource.name)

        currency_registry.register(currency_obj, name=currency_code)


def register_markets():
    for market in get_markets():
        base = market.BaseCurrency
        quote = market.MarketCurrency
        market_code = '%s%s' % (base, quote)
        market_name = '%s-%s' % (base, quote)

        if market_code not in market_registry:
            market_obj = Market(code=market_code, name=market_name, base=base, quote=quote)
        else:
            market_obj = currency_registry[market_code]

        market_obj.exchanges.append(MarketResource.name)

        market_registry.register(market_obj, name=market_code)
