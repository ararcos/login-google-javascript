import pytest
from faker import Faker
from desk_reservation.ride.application import RideUpdater


def test__ride_updater_return_ride_when_ride_is_updated(mocker, ride_factory):
    user_id = Faker().uuid4()
    ride = ride_factory()
    ride_service = mocker.Mock(
        update=mocker.Mock(return_value=ride)
    )
    ride_updater = RideUpdater(ride_service=ride_service)

    result = ride_updater.execute(
        user_id=user_id, ride_id=ride.ride_id, edited_ride=ride)

    assert ride_service.update.calledWith(
        user_id=user_id, ride_id=ride.ride_id, edited_ride=ride)
    assert result == ride


def test__ride_updater_return_none_when_ride_is_not_updated(mocker, ride_factory):
    user_id = Faker().uuid4()
    ride = ride_factory()
    ride_service = mocker.Mock(
        update=mocker.Mock(return_value=None)
    )
    ride_updater = RideUpdater(ride_service=ride_service)

    result = ride_updater.execute(
        user_id=user_id, ride_id=ride.ride_id, edited_ride=ride)

    assert ride_service.update.calledWith(
        user_id=user_id, ride_id=ride.ride_id, edited_ride=ride)
    assert result == None
