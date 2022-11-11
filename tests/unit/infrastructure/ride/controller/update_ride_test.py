import json
from typing import Callable
from http import HTTPStatus
from faker import Faker
import pytest

from desk_reservation.ride.application.ride_updater import RideUpdater
from desk_reservation.ride.infrastructure.controllers.update_ride import update_ride_controller
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError

@pytest.fixture(name="mocked_ride_updater")
def _mocked_library(mocker) -> Callable:
    def _create_ride_updater(ride_updater: any) -> None:
        mocker.patch(
            "desk_reservation.ride.infrastructure.controllers.update_ride.ride_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(RideUpdater, "execute", side_effect=ride_updater)

    return _create_ride_updater


def test__return_ride_when_ride_id_exist_an_updated_correctly(
    mocked_ride_updater, mocker, ride_factory
):
    user_id = Faker().uuid4()
    ride_id = Faker().uuid4()
    ride = ride_factory()
    event = {"body":json.dumps({**ride.__dict__, "user_id": user_id}, default=str)}
    mocked_ride_updater(mocker.Mock(return_value=ride))

    result = update_ride_controller(event)
    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps(ride.__dict__, default=str)


def test__return_not_found_when_ride_id_not_exist(
    mocked_ride_updater, mocker, ride_factory
):
    user_id = Faker().uuid4()
    ride_id = Faker().uuid4()
    ride = ride_factory()
    event = {"body":json.dumps({**ride.__dict__, "user_id": user_id}, default=str)}
    mocked_ride_updater(mocker.Mock(return_value=None))

    result = update_ride_controller(event)
    assert result["status_code"] == HTTPStatus.NOT_FOUND
    assert result["body"] == json.dumps(None)


def test__return_permission_exception_response_when_ride_is_not_updated(
    mocked_ride_updater, ride_factory
):
    user_id = Faker().uuid4()
    ride_id = Faker().uuid4()
    ride = ride_factory()
    event = {"body":json.dumps({**ride.__dict__, "user_id": user_id}, default=str)}
    mocked_ride_updater(PermissionsError("Update a ride"))

    result = update_ride_controller(event)
    assert result["status_code"] == HTTPStatus.FORBIDDEN
    assert result["body"] == json.dumps({"message": "You don't have permissions: <Update a ride>"})

def test__return_exception_validation_error_response_when_ride_is_not_updated(
    ride_factory, mocked_ride_updater, mocker
):
    ride = ride_factory()
    ride_dict = ride.__dict__
    ride_dict.pop("ride_id")
    event = {"body":json.dumps({**ride_dict, "user_id": Faker().uuid4()}, default=str)}
    mocked_ride_updater(mocker.Mock(return_value=ride))

    result = update_ride_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == json.dumps({"message": "Check Ride Attributes"})
