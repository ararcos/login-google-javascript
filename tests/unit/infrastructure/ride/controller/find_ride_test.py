import json
from typing import Callable
from http import HTTPStatus
import pytest

from desk_reservation.ride.application.ride_finder import RideFinder
from desk_reservation.ride.infrastructure.controllers.find_ride import find_ride_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from faker import Faker

@pytest.fixture(name="mocked_ride_finder")
def _mocked_library(mocker) -> Callable:
    def _create_ride_finder(ride_finder: any) -> None:
        mocker.patch(
            "desk_reservation.ride.infrastructure.controllers.find_ride.ride_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(RideFinder, "execute", side_effect=ride_finder)

    return _create_ride_finder


def test__return_list_when_ride_has_data(mocked_ride_finder, mocker, ride_factory):
    ride_id = Faker().uuid4()
    rides = ride_factory(
        ride_id = ride_id
    )
    mocked_ride_finder(mocker.Mock(return_value=[rides]))
    event = {
        "queryStringParameters": {
            "filters": [
                {"field": "ride_id", "value": ride_id, "operator": "EQUAL"}
            ]
        }
    }

    result = find_ride_controller(event)
    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps([rides.__dict__], default=str)


def test__return_empty_list_when_ride_has_not_data(mocked_ride_finder, mocker):
    rides = []
    mocked_ride_finder(mocker.Mock(return_value=rides))
    event = mocker.Mock()
    result = find_ride_controller(event)
    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps(rides)

def test__return_permission_exception_response_when_rides_have_an_error(
    mocked_ride_finder, mocker
):
    event = mocker.Mock()
    mocked_ride_finder(DomainError("Server Error"))

    result = find_ride_controller(event)
    assert result["status_code"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert result["body"] == json.dumps({"message": "Server Error"})
