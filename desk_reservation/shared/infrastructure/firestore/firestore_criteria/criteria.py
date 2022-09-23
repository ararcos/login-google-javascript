import typing
from dataclasses import dataclass

from .filter import Filter


@dataclass
class Criteria:
    filters: typing.List[Filter]
    limit: typing.Optional[int] = None
    offset: typing.Optional[int] = None
