import pytest
from faker import Faker

from desk_reservation.users.domain import User

faker = Faker()


@pytest.fixture
def user_factory():
    def _factory(**kwargs):
        args = {
            **{
                'google_id': faker.uuid4(),
                'name': faker.name(),
                'preferred_office': faker.city(),
                'email': faker.email(),
                'deleted': False,
                'language': faker.word(),
                'admin': faker.boolean(),
                "photo_url": faker.sentence(10),
                "autoSave": faker.pybool()
            },
            **kwargs
        }
        return User(**args)

    return _factory
