import pytest
from desk_reservation.ride.application.ride_finder import RideFinder


def test__ride_finder_return_list_of_rides_when_rides_exist(mocker, ride_factory, user_factory):
    criteria = mocker.Mock()
    user = user_factory()
    ride = ride_factory()
    ride_service = mocker.Mock(
        find_all=mocker.Mock(return_value=[ride]),
        populate_user_info=mocker.Mock(return_value=user)
    )
    ride_finder = RideFinder(ride_service=ride_service)

    result = ride_finder.execute(criteria=criteria)

    assert ride_service.find_all.calledWith(criteria=criteria)
    assert ride_service.populate_user_info.calledWith(ride.offerer_user_id)
    assert ride_service.populate_user_info.call_count == 1
    assert result == [{
        'rideInfo': ride,
        'userInfo': user.__dict__
    }]


def test__ride_finder_return_empty_list_when_ride_not_exist(mocker):
    criteria = mocker.Mock()
    ride_service = mocker.Mock(
        find_all=mocker.Mock(return_value=[]),
        populate_user_info=mocker.Mock(return_value=None)
    )
    ride_finder = RideFinder(ride_service=ride_service)

    result = ride_finder.execute(criteria=criteria)

    assert ride_service.find_all.calledWith(criteria=criteria)
    assert ride_service.populate_user_info.called is False
    assert not result
