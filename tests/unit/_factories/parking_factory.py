from datetime import datetime, timedelta
import pytest
from faker import Faker

from desk_reservation.parkings.domain import Parking

faker = Faker()


@pytest.fixture
def parking_factory():
    def _factory(**kwargs):
        args = {
            **{
                'parking_id': faker.uuid4(),
                'office_id': faker.uuid4(),
                'floor': faker.random_int(),
                'deleted_at': datetime.today() - timedelta(hours=1),
                'name': faker.name(),
                'created_at': datetime.now(),
                'position': [faker.random_int(), faker.random_int()]
            },
            **kwargs
        }
        return Parking(**args)

    return _factory
