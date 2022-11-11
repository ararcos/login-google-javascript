from http import HTTPStatus
import json
from typing import Callable
import pytest

from desk_reservation.ride.application.ride_booking_create import RideBookingCreator
from desk_reservation.ride.infrastructure.controllers.create_ride_booking import (
    create_ride_booking_controller,
)
from desk_reservation.shared.domain.exceptions import DomainError, BadRequestError


@pytest.fixture(name="mocked_ride_booking_creator")
def _mocked_library(mocker) -> Callable:
    def _create_ride_booking_creator(ride_booking_creator: any) -> None:
        mocker.patch(
            "desk_reservation.ride.infrastructure.controllers.create_ride_booking.ride_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(
            RideBookingCreator, "execute", side_effect=ride_booking_creator
        )

    return _create_ride_booking_creator


def test__create_ride_booking_return_not_found_response_when_ride_is_not_found(
    ride_booking_factory, mocked_ride_booking_creator, mocker
):
    ride_booking = ride_booking_factory()
    ride_booking_dict = ride_booking.__dict__
    event = {"body":json.dumps({**ride_booking_dict, "extra_seats": 1}, default=str)}
    mocked_ride_booking_creator(mocker.Mock(return_value=None))

    result = create_ride_booking_controller(event)
    assert result["status_code"] == HTTPStatus.NOT_FOUND
    assert result["body"] == json.dumps({"message": "Ride not found"})


def test__create_ride_booking_return_ride_response_when_ride_is_found(
    ride_booking_factory, mocked_ride_booking_creator, mocker
):
    ride_booking = ride_booking_factory()
    ride_booking_dict = ride_booking.__dict__
    event = {"body":json.dumps({**ride_booking_dict, "extra_seats": 1}, default=str)}
    mocked_ride_booking_creator(mocker.Mock(return_value=ride_booking))

    result = create_ride_booking_controller(event)
    assert result["status_code"] == HTTPStatus.CREATED
    assert result["body"] == json.dumps(ride_booking_dict, default=str)


def test__create_ride_booking_return_bad_request_when_ride_has_errors(
    ride_booking_factory, mocked_ride_booking_creator
):
    ride_booking = ride_booking_factory()
    ride_booking_dict = ride_booking.__dict__
    event = {"body":json.dumps({**ride_booking_dict, "extra_seats": 1}, default=str)}
    mocked_ride_booking_creator(BadRequestError("Bad Request"))

    result = create_ride_booking_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == json.dumps({"message": "Bad Request"})


def test__create_ride_booking_return_domain_error_when_ride_has_errors(
    ride_booking_factory, mocked_ride_booking_creator
):
    ride_booking = ride_booking_factory()
    ride_booking_dict = ride_booking.__dict__
    event = {"body":json.dumps({**ride_booking_dict, "extra_seats": 1}, default=str)}
    mocked_ride_booking_creator(DomainError("Bad Request"))

    result = create_ride_booking_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == json.dumps({"message": "Bad Request"})


def test__create_ride_booking_return_exception_validation_error_response_when_ride_is_has_errors_in_the_fields(
    ride_booking_factory, mocked_ride_booking_creator, mocker
):
    ride_booking = ride_booking_factory()
    ride_booking_dict = ride_booking.__dict__
    ride_booking_dict.pop("ride_id")
    event = {"body":json.dumps({**ride_booking_dict, "extra_seats": 1}, default=str)}
    mocked_ride_booking_creator(mocker.Mock(return_value=ride_booking))

    result = create_ride_booking_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == json.dumps({"message": "Check Ride Attributes"})


def test__create_ride_booking_return_exception_validation_error_response_when_event_dont_have_extra_seats(
    ride_booking_factory, mocked_ride_booking_creator, mocker
):
    ride_booking = ride_booking_factory()
    event = {"body":json.dumps({**ride_booking.__dict__}, default=str)}
    mocked_ride_booking_creator(mocker.Mock(return_value=ride_booking))

    result = create_ride_booking_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == json.dumps({"message": "Check Ride Attributes"})
