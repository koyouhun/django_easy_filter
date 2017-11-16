from .parser import Parser
from .prefix import Prefix

__version__ = "0.0.1"


def to_filter(expression):
    prefix = Prefix().to_prefix(expression)
    return Parser().parse_filter(prefix)