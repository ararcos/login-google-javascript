import json
import pytest
from typing import Callable
from http import HTTPStatus
from faker import Faker
from desk_reservation.bookings.application.booking_updater import BookingUpdater
from desk_reservation.bookings.infrastructure.controllers.update_booking import (
    update_booking_controller,
)
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError


@pytest.fixture(name="mocked_booking_updater")
def _mocked_library(mocker) -> Callable:
    def _create_booking_updater(booking_updater: any) -> None:
        mocker.patch(
            "desk_reservation.bookings.infrastructure.controllers"
            ".update_booking.booking_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(BookingUpdater, "execute", side_effect=booking_updater)

    return _create_booking_updater


def test__update_booking_controller__return_booking_updated(
    mocked_booking_updater, mocker, seat_booking_factory
):
    booking = seat_booking_factory()
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()
    event = {
        "body": json.dumps(
            {**booking.__dict__, "user_id": user_id, "booking_id": booking_id}, default=str
        )
    }
    mocked_booking_updater(mocker.Mock(return_value=booking))

    result = update_booking_controller(event)

    assert result["status_code"] == HTTPStatus.OK
    assert result["body"] == json.dumps(booking.__dict__, default=str)


def test__update_booking_controller__raises_id_not_found_error(
    mocked_booking_updater, seat_booking_factory
):
    booking = seat_booking_factory()
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()
    event = {
        "body": json.dumps(
            {**booking.__dict__, "user_id": user_id, "booking_id": booking_id}, default=str
        )
    }
    mocked_booking_updater(IdNotFoundError("Booking not found", booking_id))

    result = update_booking_controller(event)

    assert result["status_code"] == HTTPStatus.NOT_FOUND
    assert result["body"] == json.dumps(
        {"message": "Booking not found id:'" + booking_id + "' not found"}
    )


def test__update_booking_controller__raises_domain_error(
    mocked_booking_updater, seat_booking_factory
):
    booking = seat_booking_factory()
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()
    event = {
        "body": json.dumps(
            {**booking.__dict__, "user_id": user_id, "booking_id": booking_id}, default=str
        )
    }
    mocked_booking_updater(DomainError("Internal error"))

    result = update_booking_controller(event)

    assert result["status_code"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert result["body"] == '{"message": "Internal error"}'


def test__return_exception_validation_error_response_when_booking_is_not_updated(
    seat_booking_factory, mocked_booking_updater, mocker
):
    booking = seat_booking_factory()
    booking_dict = booking.__dict__
    booking_dict.pop("booking_id")
    event = booking_dict
    mocked_booking_updater(mocker.Mock(return_value=booking))

    result = update_booking_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == '{"message": "Check Booking Attributes"}'
