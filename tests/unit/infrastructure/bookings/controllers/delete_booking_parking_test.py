import json
from typing import Callable
from http import HTTPStatus
import pytest
from faker import Faker
from desk_reservation.bookings.application.booking_parking_deleter import (
    BookingParkingDeleter,
)
from desk_reservation.bookings.infrastructure.controllers.delete_booking_parking import (
    delete_booking_parking_controller,
)

from desk_reservation.shared.domain.exceptions.domain_error import DomainError


@pytest.fixture(name="mocked_booking_deleter")
def _mocked_library(mocker) -> Callable:
    def _create_booking_deleter(delete_parking_booking: any) -> None:
        mocker.patch(
            "desk_reservation.bookings.infrastructure.controllers"
            ".delete_booking_parking.booking_parking_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(
            BookingParkingDeleter, "execute", side_effect=delete_parking_booking
        )

    return _create_booking_deleter


def test__delete_booking_controller__return_true_when_is_deleted(
    mocked_booking_deleter,
    mocker,
):
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()
    event = {"body": json.dumps({"user_id": user_id, "booking_id": booking_id})}

    mocked_booking_deleter(mocker.Mock(return_value=True))

    result = delete_booking_parking_controller(event)

    assert result["status_code"] == HTTPStatus.OK
    assert json.loads(result["body"]) is True


def test__delete_booking_controller__raises_domain_error(
    mocked_booking_deleter,
):
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()
    event = {"body": json.dumps({"user_id": user_id, "booking_id": booking_id})}

    mocked_booking_deleter(DomainError("Internal server error"))

    result = delete_booking_parking_controller(event)

    assert result["status_code"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert result["body"] == '{"message": "Internal server error"}'
