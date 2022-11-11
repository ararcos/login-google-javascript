import json
from typing import Callable
from http import HTTPStatus
import pytest
from faker import Faker
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.bookings.application.booking_parking_finder import (
    BookingParkingFinder,
)
from desk_reservation.bookings.infrastructure.controllers.find_booking_parking import (
    find_booking_parking_controller,
)


@pytest.fixture(name="mocked_booking_parking_finder")
def _mocked_library(mocker) -> Callable:
    def _create_booking_finder(find_parking_bookings: any) -> None:
        mocker.patch(
            "desk_reservation.bookings.infrastructure.controllers"
            ".find_booking_parking.booking_parking_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(
            BookingParkingFinder, "execute", side_effect=find_parking_bookings
        )

    return _create_booking_finder


def test__find_booking_parking_controller__return_booking_parkings(
    mocked_booking_parking_finder, mocker, parking_booking_factory
):
    booking_id = Faker().uuid4()
    booking_parking = parking_booking_factory(booking_id=booking_id)
    mocked_booking_parking_finder(mocker.Mock(return_value=[booking_parking]))
    event = {
        "queryStringParameters": {
            "filters": [
                {"field": "booking_id", "value": booking_id, "operator": "EQUAL"}
            ]
        }
    }

    result = find_booking_parking_controller(event)
    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps([booking_parking.__dict__], default=str)


def test__find_booking_parking_controller__do_not_return_booking_parkings(
    mocked_booking_parking_finder,
    mocker,
):
    mocked_booking_parking_finder(mocker.Mock(return_value=[]))
    event = {"filters": {"items": mocker.Mock()} for _ in range(3)}

    result = find_booking_parking_controller(event)
    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps([])


def test__find_booking_parkingy_controller__raises_domain_error(
    mocked_booking_parking_finder,
    mocker,
):
    mocked_booking_parking_finder(DomainError("Internal server error"))
    event = {"filters": {"items": mocker.Mock()} for _ in range(3)}

    result = find_booking_parking_controller(event)
    assert result["status_code"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert result["body"] == json.dumps({"message": "Internal server error"})
