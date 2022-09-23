import pydantic
# pylint: disable=E1101

class User(pydantic.BaseModel):
    google_id: str
    name: str
    preferred_office: str
    email: str
    language: str
    deleted: bool
    admin: bool
