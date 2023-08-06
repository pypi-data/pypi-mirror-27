from .resources import CurrencyResource, MarketResource, TickerResource
from .utils import register_currencies, register_markets

__all__ = ['CurrencyResource', 'MarketResource', 'TickerResource']

# register_currencies()
register_markets()
