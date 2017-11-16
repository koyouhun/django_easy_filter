import re
from .base import OPERATION, CONNECT_FILTER, FILTER


class Prefix:
    def __init__(self):
        self.OPERATION = OPERATION
        self.CONNECT_FILTER = CONNECT_FILTER
        self.FILTER = FILTER

    def to_prefix(self, raw_filter):
        operator_list = self.OPERATION + ['(', ')']
        filter_list = self.split_filter(raw_filter)

        operands = list()
        operators = list()
        for x in filter_list:
            x = x.upper()
            # check operand
            if x not in operator_list:
                operands.append(x)

            # check parentheses
            elif x == '(' or len(operators) == 0 or self.cmp(x, operators[-1]):
                operators.append(x)

            elif x == ')':
                while operators[-1] != '(':
                    operator = operators.pop()
                    right = operands.pop()
                    left = operands.pop()
                    operands.append([operator, left, right])
                operators.pop()

            elif not self.cmp(x, operators[-1]):
                while len(operators) > 0 and \
                        not self.cmp(x, operators[-1]):
                    operator = operators.pop()
                    right = operands.pop()
                    left = operands.pop()
                    operands.append([operator, left, right])
                operators.append(x)
            else:
                raise ValueError("Wrong expression.")

        while len(operators) > 0:
            operator = operators.pop()
            right = operands.pop()
            left = operands.pop()
            operands.append([operator, left, right])
        return operands.pop()

    def cmp(self, x, y):
        return self.get_priority(x) > self.get_priority(y)

    def get_priority(self, x):
        if x in ['(', ')']:
            return 0
        elif x in ['OR', '|', '||']:
            return 1
        elif x in ['AND', '&', '&&']:
            return 2
        elif x in self.FILTER:
            return 3
        else:
            raise ValueError("Unknown filter")

    @staticmethod
    def split_filter(raw_filter):
        return re.findall("[a-zA-Z0-9_.]+|[!<>~&|=]+|[()]", raw_filter)
