import json
import pytest
from typing import Callable
from http import HTTPStatus
from faker import Faker
from desk_reservation.bookings.application import LockDeleter
from desk_reservation.bookings.infrastructure.controllers.delete_lock import (
    delete_lock_controller,
)
from desk_reservation.shared.domain.exceptions.domain_error import DomainError


@pytest.fixture(name="mocked_lock_deleter")
def _mocked_library(mocker) -> Callable:
    def _create_booking_deleter(lock_deleter: any) -> None:
        mocker.patch(
            "desk_reservation.bookings.infrastructure.controllers.delete_lock.lock_booking_service_factory",
            return_value=mocker.Mock(),
        )
        mocker.patch.object(LockDeleter, "execute", side_effect=lock_deleter)

    return _create_booking_deleter


def test__delete_lock_booking_controller__return_true_when_is_deleted(
    mocked_lock_deleter,
    mocker,
):
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()
    event = {"body": json.dumps({"user_id": user_id, "booking_id": booking_id})}

    mocked_lock_deleter(mocker.Mock(return_value=True))

    result = delete_lock_controller(event)

    assert result["status_code"] == HTTPStatus.OK
    assert json.loads(result["body"]) is True


def test__delete_lock_booking_controller__raises_domain_error(
    mocked_lock_deleter,
):
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()
    event = {"body": json.dumps({"user_id": user_id, "booking_id": booking_id})}

    mocked_lock_deleter(DomainError("Internal server error"))

    result = delete_lock_controller(event)

    assert result["status_code"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert result["body"] == '{"message": "Internal server error"}'
