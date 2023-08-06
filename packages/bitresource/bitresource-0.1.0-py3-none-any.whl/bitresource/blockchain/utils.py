from bitresource import currency_registry
from bitutils.objects import Currency
from .resources import CurrencyResource


def get_currencies():
    return list(CurrencyResource.data())


def register_currencies():
    for currency in get_currencies():
        currency_code = currency._key

        if currency_code not in currency_registry:
            currency_obj = Currency(code=currency_code, symbol=currency.symbol)
        else:
            currency_obj = currency_registry[currency_code]

        currency_obj.exchanges.append(CurrencyResource.name)

        currency_registry.register(currency_obj, name=currency_code)
