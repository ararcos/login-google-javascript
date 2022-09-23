from .domain_error import DomainError


class DbError(DomainError):
    def __init__(self):
        super().__init__("Database error")
