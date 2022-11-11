from datetime import datetime, timedelta

import pytest
from faker import Faker

from desk_reservation.bookings.domain.entities import (
    SeatBooking,
    LockBooking,
    ParkingBooking,
)

faker = Faker()


@pytest.fixture
def seat_booking_factory():
    def _factory(**kwargs):
        args = {
            **{
                "booking_id": faker.uuid4(),
                "office_id": faker.uuid4(),
                "booked_by": {
                    "google_id": faker.uuid4(),
                    "photo_url": faker.image_url(),
                    "name": faker.name(),
                },
                "booked_date_init": datetime.today(),
                "booked_date_end": datetime.today() + timedelta(hours=1),
                "desk_id": faker.uuid4(),
                "seat_id": faker.uuid4(),
                "has_pet": faker.boolean(),
                "has_child": faker.boolean(),
            },
            **kwargs,
        }
        return SeatBooking(**args)

    return _factory


@pytest.fixture
def parking_booking_factory():
    def _factory(**kwargs):
        args = {
            **{
                "booking_id": faker.uuid4(),
                "office_id": faker.uuid4(),
                "booked_by": {
                    "google_id": faker.uuid4(),
                    "photo_url": faker.image_url(),
                    "name": faker.name(),
                },
                "booked_date_init": datetime.today(),
                "booked_date_end": datetime.today() + timedelta(hours=1),
                "parking_id": faker.uuid4(),
            },
            **kwargs,
        }
        return ParkingBooking(**args)

    return _factory


@pytest.fixture
def lock_booking_factory():
    def _factory(**kwargs):
        args = {
            **{
                "booking_id": faker.uuid4(),
                "office_id": faker.uuid4(),
                "locked_by": {
                    "google_id": faker.uuid4(),
                    "photo_url": faker.image_url(),
                    "name": faker.name(),
                },
                "booked_date_init": datetime.today(),
                "booked_date_end": datetime.today() + timedelta(hours=1),
                "desk_id": faker.uuid4(),
                "seat_id": faker.uuid4(),
            },
            **kwargs,
        }
        return LockBooking(**args)

    return _factory
