import pytest
from faker import Faker
from desk_reservation.ride.application.ride_finder_by_id import RideFinderById


def test__ride_finder_by_id_return_ride_when_ride_exist(mocker, ride_factory, user_factory):
    user = user_factory()
    ride = ride_factory()
    ride_service = mocker.Mock(
        find_by_id=mocker.Mock(return_value=ride),
        populate_user_info=mocker.Mock(return_value=user)
    )
    ride_finder_by_id = RideFinderById(ride_service=ride_service)

    result = ride_finder_by_id.execute(ride.ride_id)

    assert ride_service.find_by_id.calledWith(ride_id=ride.ride_id)
    assert ride_service.populate_user_info.calledWith(ride.offerer_user_id)
    assert ride_service.populate_user_info.call_count == 1
    assert result == {
        'rideInfo': ride,
        'userInfo': user.__dict__
    }


def test__ride_finder_by_id_return_none_when_ride_not_exist(mocker):
    ride_id = Faker().uuid4()
    ride_service = mocker.Mock(
        find_by_id=mocker.Mock(return_value=[]),
        populate_user_info=mocker.Mock(return_value=None)
    )
    ride_finder_by_id = RideFinderById(ride_service=ride_service)

    result = ride_finder_by_id.execute(ride_id)

    assert ride_service.find_by_id.calledWith(ride_id=ride_id)
    assert ride_service.populate_user_info.called is False
    assert result is None
