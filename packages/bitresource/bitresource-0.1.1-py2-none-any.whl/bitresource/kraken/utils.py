from bitresource import currency_registry, market_registry
from bitutils.objects import Currency, Market
from .resources import CurrencyResource, MarketResource


def get_currencies():
    return list(CurrencyResource.data())


def get_markets():
    return list(MarketResource.data())


def register_currencies():
    for currency in get_currencies():
        currency_code = currency.altname

        if currency_code not in currency_registry:
            currency_obj = Currency(code=currency_code, decimals=currency.decimals)
        else:
            currency_obj = currency_registry[currency_code]

        currency_obj.exchanges.append(CurrencyResource.name)

        currency_registry.register(currency_obj, name=currency_code)


def register_markets():
    for market in get_markets():
        base_name = market.base
        currency_name = market.quote[1:]
        market_code = market.altname

        if base_name.startswith('X'):
            base_name = base_name[1:]

        if market_code not in market_registry:
            market_obj = Market(code=market_code, name='%s-%s' % (base_name, currency_name), base=base_name,
                                currency=currency_name)
        else:
            market_obj = currency_registry[market_code]

        market_obj.exchanges.append(MarketResource.name)

        market_registry.register(market_obj, name=market_code)
