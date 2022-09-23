from ....shared.domain.exceptions import DomainError


class IncorrectDomainError(DomainError):
    def __init__(self):
        message = "The Domain must be @ioet.com"
        super().__init__(409, message)
