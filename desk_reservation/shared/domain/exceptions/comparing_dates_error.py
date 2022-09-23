from .domain_error import DomainError


class ComparingDatesError(DomainError):
    def __init__(self):
        super().__init__("The end date and the init date are not valid")
