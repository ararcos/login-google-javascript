from .domain_error import DomainError


class IdNotFoundError(DomainError):
    def __init__(self, entity: str, entity_id: str):
        super().__init__(f"{entity} id:'{entity_id}' not found")
