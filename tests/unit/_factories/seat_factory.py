from datetime import datetime, timedelta
import pytest
from faker import Faker

from desk_reservation.seats.domain import Seat

faker = Faker()


@pytest.fixture
def seat_factory():
    def _factory(**kwargs):
        args = {
            **{
                'seat_id': faker.uuid4(),
                'desk_id': faker.uuid4(),
                'office_id': faker.uuid4(),
                'name': faker.name(),
                'deleted_at': datetime.today() - timedelta(hours=1),
                'is_laptop': faker.boolean(),
                'created_at': datetime.now(),
                'position': [faker.random_int(),faker.random_int()],
                "leftPixels": faker.pyfloat(),
                "topPixels": faker.pyfloat(),
            },
            **kwargs
        }
        return Seat(**args)

    return _factory
