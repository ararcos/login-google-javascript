import pytest
from faker import Faker
from desk_reservation.ride.application import RideDeleter


def test__ride_deleter_return_true_when_ride_is_deleted(mocker, ride_factory):
    user_id = Faker().uuid4()
    ride = ride_factory()
    ride_service = mocker.Mock(
        delete=mocker.Mock(return_value=True)
    )
    ride_deleter = RideDeleter(ride_service=ride_service)

    result = ride_deleter.execute(ride_id=ride.ride_id, user_id=user_id)

    assert result is True


def test__ride_deleter_return_false_when_ride_is_not_deleted(mocker, ride_factory):
    user_id = Faker().uuid4()
    ride = ride_factory()
    ride_service = mocker.Mock(
        delete=mocker.Mock(return_value=False)
    )
    ride_deleter = RideDeleter(ride_service=ride_service)

    result = ride_deleter.execute(ride_id=ride.ride_id, user_id=user_id)

    assert result is False
