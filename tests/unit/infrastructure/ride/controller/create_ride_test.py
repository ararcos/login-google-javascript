from http import HTTPStatus
import json
from typing import Callable
import pytest

from desk_reservation.ride.application.ride_creator import RideCreator
from desk_reservation.shared.domain.exceptions.bad_request import BadRequestError
from desk_reservation.ride.infrastructure.controllers.create_ride import (
    create_ride_controller,
)


@pytest.fixture(name="mocked_ride_creator")
def _mocked_library(mocker) -> Callable:
    def _create_ride_creator(ride_creator: any) -> None:
        mocker.patch(
            "desk_reservation.ride.infrastructure.controllers.create_ride.ride_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(RideCreator, "execute", side_effect=ride_creator)

    return _create_ride_creator


def test__return_valid_response_when_desk_is_created(
    mocked_ride_creator, mocker, ride_factory
):
    ride = ride_factory()
    event = {"body":json.dumps({**ride.__dict__}, default=str)}
    mocked_ride_creator(mocker.Mock(return_value=ride))
    result = create_ride_controller(event)
    assert result["status_code"] == HTTPStatus.CREATED
    assert result["body"] == json.dumps(ride.__dict__, default=str)


def test__return_exception_validation_error_response_when_ride_is_not_created(
    ride_factory, mocked_ride_creator, mocker
):
    ride = ride_factory()
    ride_dict = ride.__dict__
    ride_dict.pop("ride_id")
    event = {"body":json.dumps({**ride.__dict__}, default=str)}
    mocked_ride_creator(mocker.Mock(return_value=ride))

    result = create_ride_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == json.dumps({"message": "Check Ride Attributes"})


def test__return_bad_request_exception_response_when_ride_is_not_created(
    mocked_ride_creator, ride_factory
):
    ride = ride_factory()
    event = {"body":json.dumps({**ride.__dict__}, default=str)}
    mocked_ride_creator(BadRequestError("Ride is old"))

    result = create_ride_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert json.loads(result["body"]) == {"message": "Ride is old"}
