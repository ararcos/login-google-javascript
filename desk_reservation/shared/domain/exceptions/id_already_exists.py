from .domain_error import DomainError


class IdAlreadyExists(DomainError):
    def __init__(self, entity: str):
        super().__init__(f"Cannot create a new <{entity}>, Id already exists")
