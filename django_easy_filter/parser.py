import six
from django.db.models import Q
from .base import CONNECT_FILTER, FILTER


class Parser:
    def __init__(self):
        self.CONNECT_FILTER = CONNECT_FILTER
        self.FILTER = FILTER

    def parse_filter(self, prefix_expression):
        if len(prefix_expression) != 3:
            raise ValueError("wrong expression.")

        operator = prefix_expression[0]
        left = prefix_expression[1]
        right = prefix_expression[2]

        if isinstance(left, six.string_types):
            left = left.replace('.', '__')

        if not isinstance(operator, six.string_types):
            raise ValueError("Wrong expression or Wrong custom prefix converter")

        operator = operator.upper()

        if operator in self.CONNECT_FILTER:
            return self.connect_filter_handler(operator, left, right)
        elif operator in self.FILTER:
            return self.filter_handler(operator, left, right)

    def connect_filter_handler(self, operator, left, right):
        if not (isinstance(left, list) and isinstance(right, list)):
            raise ValueError("Wrong connect filter. Check AND/OR.")

        if isinstance(left, list):
            left = self.parse_filter(left)
        if isinstance(right, list):
            right = self.parse_filter(right)

        if operator in ['AND', '&', '&&']:
            return left & right
        elif operator in ['OR', '|', '||']:
            return left | right
        else:
            raise ValueError("Unknown connect operator")

    @staticmethod
    def filter_handler(operator, left, right):
        if not (isinstance(left, six.string_types) and isinstance(right, six.string_types)):
            raise ValueError("Wrong filter. Check =, !=, <, >, ...")

        if operator in ['=', '==', '===']:
            return Q(**{left: right})
        elif operator in ['!=', '<>']:
            return ~Q(**{left: right})
        elif operator == '>':
            return Q(**{left + '__gt': right})
        elif operator == '>=':
            return Q(**{left + '__gte': right})
        elif operator == '<':
            return Q(**{left + '__lt': right})
        elif operator == '<=':
            return Q(**{left + '__lte': right})
        elif operator == '~=':
            left_percent = right.startswith("%")
            right_percent = right.endswith("%")
            if left_percent and not right_percent:
                return Q(**{left + '__iendswith': right})
            elif not left_percent and right_percent:
                return Q(**{left + '__istartswith': right})
            else:
                return Q(**{left + '__icontains': right})
        else:
            raise ValueError("Unknown operator")
