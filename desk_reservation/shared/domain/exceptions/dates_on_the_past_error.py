from .domain_error import DomainError


class DatesOnThePastError(DomainError):
    def __init__(self):
        super().__init__("You can't book on the past")
