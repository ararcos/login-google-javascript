from datetime import date, timedelta
from inspect import signature
import random

import pytest
from faker import Faker
from desk_reservation.desks.domain.entities.desk import Desk
from desk_reservation.offices.domain.entities.office import Office
from desk_reservation.parkings.domain.entities.parking import Parking
from desk_reservation.ride.domain.entities.ride import Ride
from desk_reservation.seats.domain.entities.seat import Seat
from desk_reservation.users.domain.entities.user import User
from desk_reservation.bookings.domain.entities import Booking


def mock_thing(thing, **kwargs):
    args = []
    for argument in signature(thing).parameters:
        if argument in kwargs:
            args.append(kwargs[argument])
        else:
            args.append(None)

    return thing(*args)


@pytest.fixture
def make_booking():
    def _make_booking(
        booking_id=Faker().random_int(),
        spot_id=Faker().uuid4(),
        booked_by=Faker().uuid4(),
        booked_date_end=Faker().future_date(),
        booked_date_init=date.today(),
    ):
        faker = Faker()
        booking_default = {
            "booking_id": booking_id,
            "office_id": faker.uuid4(),
            "desk_id": faker.uuid4(),
            "spot_id": spot_id,
            "booked_by": booked_by,
            "booked_date_init": booked_date_init,
            "booked_date_end": booked_date_end,
            "has_pet": faker.boolean(),
            "has_child": faker.boolean(),
            "is_locked": faker.boolean(),
        }
        return mock_thing(Booking, **booking_default)

    return _make_booking


@pytest.fixture
def make_ride():
    def _make_ride(
        ride_id=Faker().uuid4(),
        offerer_user_id=Faker().uuid4(),
        departure_time=Faker().time(),
        ride_date=date.today() + timedelta(days=1),
        departure_point=Faker().uuid4(),
        destiny_office=Faker().uuid4(),
        total_spots=Faker().random_int(),
        passengers_user_id=[Faker().uuid4(), Faker().uuid4()],
    ):
        ride_default = {
            "ride_id": ride_id,
            "offerer_user_id": offerer_user_id,
            "ride_date": ride_date,
            "departure_time": departure_time,
            "departure_point": departure_point,
            "destiny_office": destiny_office,
            "total_spots": total_spots,
            "passengers_user_id": passengers_user_id,
        }
        return mock_thing(Ride, **ride_default)

    return _make_ride


@pytest.fixture
def make_desk():
    def _make_desk(
        desk_id=Faker().uuid4(),
        desk_name=Faker().name(),
        top_pixel=str(Faker().random.randint(1, 100)),
        left_pixel=str(Faker().random.randint(1, 100)),
        width=str(Faker().random.randint(1, 100)),
        height=str(Faker().random.randint(1, 100)),
        seats_list=["1", "2", "3", "4"],
        office_id=Faker().uuid4(),
    ):
        desk_default = {
            "desk:id": desk_id,
            "desk_name": desk_name,
            "top_pixel": top_pixel,
            "left_pixel": left_pixel,
            "width": width,
            "height": height,
            "seats_list": seats_list,
            "office_id": office_id,
        }
        return mock_thing(Desk, **desk_default)

    return _make_desk


@pytest.fixture
def make_parking():
    def _make_parking(
        parking_id=Faker().uuid4(),
        office_id=Faker().uuid4(),
        floor=random.randint(1, 10),
        name=Faker().name(),
        deleted_at=date.today(),
    ):
        parking_default = {
            "parking_id": parking_id,
            "office_id": office_id,
            "floor": floor,
            "name": name,
            "deleted_at": deleted_at,
        }
        return mock_thing(Parking, **parking_default)

    return _make_parking


@pytest.fixture
def make_seat():
    def _make_seat(
        name=Faker().uuid4(),
        position=Faker().uuid4(),
        setup=Faker().uuid4(),
        seat_id=Faker().uuid4(),
        desk_id=Faker().uuid4(),
    ):
        seat_default = {
            "name": name,
            "position": position,
            "setup": setup,
            "seat_id": seat_id,
            "desk_id": desk_id,
        }
        return mock_thing(Seat, **seat_default)

    return _make_seat
