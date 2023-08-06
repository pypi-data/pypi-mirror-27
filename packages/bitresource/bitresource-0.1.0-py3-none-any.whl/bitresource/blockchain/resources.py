from bitresource import resource_registry
from dictutils import AttrDict
from http_resource import HttpResource


@resource_registry.register()
class BlockchainResource(HttpResource):
    name = 'blockchain'
    endpoint_url = 'https://blockchain.info/'

    def results_iter(self, response, **kwargs):
        results = response.json()

        if type(results) is dict:
            if 'result' in results:
                results = results.get('result')
                if type(results) is dict:
                    results = [dict({'_key': k}, **v) for (k, v) in results.items()]
            else:
                results = list(results.items())

        for result in results:

            if type(result) is tuple:
                result[1].update({'_key': result[0]})
                yield AttrDict(result[1])
            else:
                yield AttrDict(result)


CurrencyResource = BlockchainResource('ticker')

TickerResource = BlockchainResource('ticker')
