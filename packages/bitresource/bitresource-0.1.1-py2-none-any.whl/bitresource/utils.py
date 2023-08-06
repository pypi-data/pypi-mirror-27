from bitresource import resource_registry, exchange_registry, currency_registry, market_registry


def register_currencies():
    for resource in resource_registry.values():
        exchange = exchange_registry.get(resource.name)

        if hasattr(resource, 'get_currencies'):
            currencies = resource.get_currencies()

            for currency in currencies:
                currency_obj = currency_registry.get(currency.code, None)

                if not currency_obj:
                    currency.exchanges = [exchange, ]
                    currency_registry.register(currency, name=currency.code)
                else:
                    exchange_keys = [exchange_item.get('code') for exchange_item in
                                     currency_registry[currency.code].exchanges]
                    if exchange.code not in exchange_keys:
                        currency_registry[currency.code].exchanges.append(exchange)


def register_markets():
    for resource in resource_registry.values():
        exchange = exchange_registry.get(resource.name)

        if hasattr(resource, 'get_markets'):
            markets = resource.get_markets()

            for market in markets:

                if market.code not in market_registry:
                    market.exchanges = [exchange, ]
                    market_registry.register(market, name=market.code)
                else:
                    market_registry[market.code].exchanges.append(exchange)
