from ....shared.domain.exceptions import DomainError


class TooManySeatsError(DomainError):
    def __init__(self, entity: str):
        super().__init__(f"Cannot create a new <{entity}>, Too many seats were added.")
