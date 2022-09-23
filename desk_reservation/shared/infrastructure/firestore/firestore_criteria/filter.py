from dataclasses import dataclass

from .operator import Operator


@dataclass()
class Filter:
    field: str
    operator: Operator
    value: str
