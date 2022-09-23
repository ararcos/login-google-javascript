from .domain_error import DomainError


class PermissionsError(DomainError):
    def __init__(self, msg):
        message = f"You don't have permissions: <{msg}>"
        super().__init__(message)
