import pytest
from faker import Faker

from desk_reservation.ride.domain import RideBooking

faker = Faker()


@pytest.fixture
def ride_booking_factory():
    def _factory(**kwargs):
        args = {
            **{
                'ride_booking_id': faker.uuid4(),
                'user_id': faker.uuid4(),
                'ride_id': faker.uuid4(),
                'user_name': faker.pystr(),
                'has_child': faker.pybool(),
                'has_pet': faker.pybool(),
                'user_photo': faker.image_url(),
                'is_extra_seat': faker.pybool(),
            },
            **kwargs
        }
        return RideBooking(**args)

    return _factory
