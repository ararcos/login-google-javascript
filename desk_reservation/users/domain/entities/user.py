import pydantic

# pylint: disable=E1101
class User(pydantic.BaseModel):
    google_id: str
    name: str
    email: str
    photo_url: str
    language: str
    deleted: bool
    admin: bool
    autoSave: bool
    preferred_office: str = None

    @pydantic.validator("deleted", pre=True, always=True)
    @classmethod
    def default_created(cls, value):
        return value or False
