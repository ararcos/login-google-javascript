import pytest
from desk_reservation.ride.application import RideCreator


def test__ride_creator_return_ride_when_ride_is_created(mocker, ride_factory):
    ride = ride_factory()
    ride_service = mocker.Mock(
        create=mocker.Mock(return_value=ride)
    )
    ride_creator = RideCreator(ride_service=ride_service)

    result = ride_creator.execute(ride_candidate=ride)

    assert ride_service.create.calledWith(ride_candidate=ride)
    assert result == ride
    