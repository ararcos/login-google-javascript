import json
import pytest
from typing import Callable
from http import HTTPStatus

from desk_reservation.bookings.application.booking_creator import BookingCreator
from desk_reservation.bookings.domain.exceptions.user_already_has_a_reservation import (
    UserAlreadyHasReservation)
from desk_reservation.bookings.infrastructure.controllers.create_booking import (
    create_book as create_booking_controller)
from desk_reservation.shared.domain.exceptions.domain_error import DomainError


@pytest.fixture(name='mocked_booking_creator')
def _mocked_library(mocker) -> Callable:
    def _create_booking_creator(booking_creator: any) -> None:
        mocker.patch('desk_reservation.bookings.infrastructure.controllers.create_booking.booking_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(BookingCreator, 'execute',
                            side_effect=booking_creator)
    return _create_booking_creator


def test__create_booking_controller__return_booking(
    mocked_booking_creator,
    mocker,
    seat_booking_factory
):
    booking = seat_booking_factory()
    mocked_booking_creator(mocker.Mock(return_value=booking))
    event = {"body":json.dumps(booking.__dict__, default=str)}
    result = create_booking_controller(event)
    assert result['status_code'] == HTTPStatus.CREATED
    assert result['body'] == json.dumps(booking.__dict__, default=str)


def test__create_booking_controller__raise_user_already_has_reservation(
    mocked_booking_creator,
    seat_booking_factory
):
    mocked_booking_creator(UserAlreadyHasReservation(
        "You must have only one booked per office on same day"))
    booking = seat_booking_factory()

    event = {"body":json.dumps(booking.__dict__, default=str)}

    result = create_booking_controller(event)

    assert result["status_code"] == HTTPStatus.BAD_REQUEST
    assert result["body"] == '{"message": "You must have only one booked per office on same day"}'


def test__create_booking_controller__raise_domain_error(
    mocked_booking_creator,
    seat_booking_factory
):
    mocked_booking_creator(DomainError("An external error ocurred"))
    booking = seat_booking_factory()
    event = {"body":json.dumps(booking.__dict__, default=str)}

    result = create_booking_controller(event)

    assert result['status_code'] == HTTPStatus.BAD_REQUEST
    assert result['body'] == '{"message": "An external error ocurred"}'


def test__return_exception_validation_error_response_when_booking_is_not_created(
    seat_booking_factory, mocked_booking_creator, mocker
):
    booking = seat_booking_factory()
    booking_dict = booking.__dict__
    booking_dict.pop("booking_id")
    event = {"body":json.dumps(booking.__dict__, default=str)}
    mocked_booking_creator(mocker.Mock(return_value=booking))

    result = create_booking_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
