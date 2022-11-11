import json
import pytest
from typing import Callable
from http import HTTPStatus

from desk_reservation.bookings.application import LockCreator
from desk_reservation.bookings.domain.exceptions.user_already_has_a_reservation import (
    UserAlreadyHasReservation)
from desk_reservation.bookings.infrastructure.controllers.create_lock import create_lock_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError


@pytest.fixture(name='mocked_lock_creator')
def _mocked_library(mocker) -> Callable:
    def _create_lock_creator(lock_creator: any) -> None:
        mocker.patch('desk_reservation.bookings.infrastructure.controllers.create_lock.lock_booking_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(LockCreator, 'execute',
                            side_effect=lock_creator)
    return _create_lock_creator


def test__create_lock_controller__return_lock_booking(
    mocked_lock_creator,
    mocker,
    lock_booking_factory
):
    lock_booking = lock_booking_factory()
    mocked_lock_creator(mocker.Mock(return_value=lock_booking))
    event = {"body":json.dumps(lock_booking.__dict__, default=str)}
    result = create_lock_controller(event)
    assert result['status_code'] == HTTPStatus.CREATED
    assert result['body'] == json.dumps(lock_booking.__dict__, default=str)


def test__create_lock_controller__raise_domain_error(
    mocked_lock_creator,
    lock_booking_factory
):
    mocked_lock_creator(DomainError("An external error ocurred"))
    lock_booking = lock_booking_factory()
    event = {"body":json.dumps(lock_booking.__dict__, default=str)}

    result = create_lock_controller(event)

    assert result['status_code'] == HTTPStatus.BAD_REQUEST
    assert result['body'] == '{"message": "An external error ocurred"}'


def test__return_exception_validation_error_response_when_lock_booking_is_not_created(
    lock_booking_factory, mocked_lock_creator, mocker
):
    lock_booking = lock_booking_factory()
    lock_booking_dict = lock_booking.__dict__
    lock_booking_dict.pop("booking_id")
    event = {"body":json.dumps(lock_booking.__dict__, default=str)}
    mocked_lock_creator(mocker.Mock(return_value=lock_booking))

    result = create_lock_controller(event)
    assert result["status_code"] == HTTPStatus.BAD_REQUEST
