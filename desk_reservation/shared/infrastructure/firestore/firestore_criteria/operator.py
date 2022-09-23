from enum import Enum


class Operator(Enum):
    EQUAL = '=='
    NOT_EQUAL = '!='
    GREATER_THAN = '>'
    LOWER_THAN = '<'
    GREATER_EQUAL_THAN = '>='
    LOWER_EQUAL_THAN = '<='
    CONTAINS = 'in'
    NOT_CONTAINS = 'not-in'
