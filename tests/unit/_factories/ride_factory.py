import pytest
from faker import Faker

from desk_reservation.ride.domain import Ride

faker = Faker()


@pytest.fixture
def ride_factory():
    def _factory(**kwargs):
        args = {
            **{
                'ride_id': faker.uuid4(),
                'offerer_user_id': faker.uuid4(),
                'ride_date': faker.future_datetime(),
                'departure_time': faker.time(),
                'departure_point': faker.pystr(),
                'destiny_office': faker.pystr(),
                'destiny_latitude': faker.pyfloat(),
                'destiny_longitude': faker.pyfloat(),
                'allow_child': faker.pybool(),
                'allow_pet': faker.pybool(),
                'total_spots': faker.pyint(),
                'passengers': [faker.pystr() for _ in range(3)],
                'created_at': faker.future_datetime(),
                'is_uber': faker.pybool()
            },
            **kwargs
        }
        return Ride(**args)

    return _factory
