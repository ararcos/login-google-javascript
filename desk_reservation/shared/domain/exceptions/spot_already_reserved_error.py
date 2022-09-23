from .domain_error import DomainError


class SpotAlreadyReservedError(DomainError):
    def __init__(self):
        super().__init__("This spot is already reserved.")
