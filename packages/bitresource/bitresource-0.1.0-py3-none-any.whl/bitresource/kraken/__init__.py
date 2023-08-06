from .resources import CurrencyResource
from .utils import register_currencies, register_markets

__all__ = ['CurrencyResource', ]

register_currencies()
register_markets()
