

from .domain_error import DomainError


class NameAlreadyExistsError(DomainError):
    def __init__(self, entity: str, name: str):
        super().__init__(f"Cannot create a new <{entity}>, Name: {name} already exists")
