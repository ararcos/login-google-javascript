from http import HTTPStatus
import json
from typing import Callable
from faker import Faker
import pytest

from desk_reservation.ride.application.ride_deleter import RideDeleter
from desk_reservation.ride.infrastructure.controllers.delete_ride import delete_ride_controller
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError


@pytest.fixture(name="mocked_ride_deleter")
def _mocked_library(mocker) -> Callable:
    def _create_ride_deleter(ride_deleter: any) -> None:
        mocker.patch(
            "desk_reservation.ride.infrastructure.controllers.delete_ride.ride_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(RideDeleter, "execute", side_effect=ride_deleter)

    return _create_ride_deleter

def test__return_true_when_ride_is_deleted(mocked_ride_deleter, mocker):
    ride_id = Faker().uuid4()
    user_id = Faker().uuid4()
    mocked_ride_deleter(mocker.Mock(return_value=True))
    event = {"body":json.dumps({"ride_id": Faker().uuid4(), "user_id": Faker().uuid4()}, default=str)}
    result = delete_ride_controller(event)
    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps(None)


def test__return_false_when_ride_is_deleted(mocked_ride_deleter, mocker):
    ride_id = Faker().uuid4()
    user_id = Faker().uuid4()
    mocked_ride_deleter(mocker.Mock(return_value=False))
    event = {"body":json.dumps({"ride_id": Faker().uuid4(), "user_id": Faker().uuid4()}, default=str)}

    result = delete_ride_controller(event)
    assert result["status_code"] == HTTPStatus.NOT_FOUND
    assert result["body"] == json.dumps(None)


def test__return_permission_exception_response_when_ride_is_not_deleted(
    mocked_ride_deleter, ride_factory
):
    desk = ride_factory()
    event = {"body":json.dumps({"ride_id": Faker().uuid4(), "user_id": Faker().uuid4()}, default=str)}
    mocked_ride_deleter(PermissionsError("Delete a Ride"))

    result = delete_ride_controller(event)
    assert result["status_code"] == HTTPStatus.FORBIDDEN
    assert result["body"] == json.dumps({"message": "You don't have permissions: <Delete a Ride>"})
