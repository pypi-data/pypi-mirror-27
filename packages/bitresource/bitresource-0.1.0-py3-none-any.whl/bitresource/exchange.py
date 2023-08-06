import inspect
import sys
from decimal import Decimal

import requests

from bitresource import bitpay
from bitresource import bitstamp
from bitresource import blockchain
from bitresource import coinbase
from bitresource import coindesk
from bitresource import kraken

DEFAULT_CURRENCIES = ['USD', 'EUR', 'TRY', 'GBP', 'JPY']


class Exchange(object):
    def fetch_data(self):
        response = requests.request('GET', self.URL, headers={'User-Agent': 'bitutils'})
        return response.json()

    def get_rates(self, includes=None, excludes=None):
        pass

    def get_currencies(self):
        rates = self.get_rates()
        return sorted([str(a) for (a, b) in rates.items() if b is not None and len(a) == 3])

    def name(self):
        return self.__class__.__name__


class BitPay(Exchange):
    def get_rates(self, includes=None, excludes=None):
        rates = bitpay.ExchangeRates.all()
        return {'BTC': dict([(r['code'], Decimal(r['rate'])) for r in rates.data])}


class BitStamp(Exchange):
    def get_rates(self, includes=None, excludes=None):
        rates = bitstamp.ExchangeRates.all()

        return {'BTC': {'USD': Decimal(rates['last'])}}


class BlockchainInfo(Exchange):
    def get_rates(self, includes=None, excludes=None):
        rates = blockchain.ExchangeRates.all()
        return {'BTC': dict([(r, Decimal(rates[r]['15m'])) for r in rates])}


class Coinbase(Exchange):
    def get_rates(self, includes=None, excludes=None):
        rates = coinbase.ExchangeRates.all()
        result = {}

        for k, v in rates.items():
            keys = k.upper().split('_')

            if keys[0] not in result:
                result[keys[0]] = {}

            result[keys[0]][keys[2]] = Decimal(v)

        return result


class CoinDesk(Exchange):
    def get_rates(self, includes=None, excludes=None):
        currencies = coindesk.Currencies.all()
        result = {}

        for c in currencies.data:
            if c.currency in includes and c.currency not in excludes:
                r = coindesk.CurrentPrice.filter(c.currency)
                result[c.currency] = Decimal(r.bpi[c.currency].rate_float)

        return {'BTC': result}


class Kraken(Exchange):
    def get_rates(self, includes=None, excludes=None):
        currencies = ['EUR', 'USD', 'CAD', 'GBP', 'JPY']

        result = {}
        for c in currencies:
            if c in includes and c not in excludes:
                rates = kraken.ExchangeRates.filter(pair='XBT%s' % c)
                result.update(dict((k[-3:], Decimal(float(v['c'][0]))) for k, v in rates['result'].items()))

        return {'BTC': result}


def get_exchanges_and_currencies():
    import os, json
    path = os.path.join(os.path.dirname(__file__), 'currencies.json')
    try:
        return json.loads(open(path, 'r').read())
    except:
        pass
    d = {}
    is_exchange = lambda obj: (inspect.isclass(obj) and issubclass(obj, Exchange) and obj != Exchange)
    exchanges = dict(inspect.getmembers(sys.modules[__name__], is_exchange))
    for name, klass in exchanges.items():
        exchange = klass()
        try:
            for k, v in exchange.get_rates(includes=DEFAULT_CURRENCIES, excludes=[]).items():
                if k not in d:
                    d[k] = {}

                for sk, sv in v.items():
                    if sk not in d[k]:
                        d[k][sk] = {}

                    d[k][sk][exchange.name()] = sv
        except Exception as e:
            continue
    # with open(path, 'w') as f:
    #     f.write(json.dumps(d, indent=4, sort_keys=True))
    return d


CURRENCIES = get_exchanges_and_currencies()

print(CURRENCIES)
