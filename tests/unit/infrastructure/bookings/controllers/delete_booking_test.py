import json
import pytest
from typing import Callable
from http import HTTPStatus
from faker import Faker
from desk_reservation.bookings.application.booking_deleter import BookingDeleter
from desk_reservation.bookings.infrastructure.controllers.delete_booking import delete_booking_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError

@pytest.fixture(name='mocked_booking_deleter')
def _mocked_library(mocker) -> Callable:
    def _create_booking_deleter(booking_deleter: any) -> None:
        mocker.patch('desk_reservation.bookings.infrastructure.controllers.delete_booking.booking_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(BookingDeleter, 'execute',
                            side_effect=booking_deleter)
    return _create_booking_deleter

def test__delete_booking_controller__return_true_when_is_deleted(
    mocked_booking_deleter,
    mocker,
    seat_booking_factory
):
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()
    booking = seat_booking_factory(
        booking_id=booking_id,
        user_id=user_id
    )
    event = {"body":json.dumps({"user_id": user_id, "booking_id": booking_id})}

    mocked_booking_deleter(mocker.Mock(return_value=True))

    result = delete_booking_controller(event)

    assert result["status_code"] == HTTPStatus.OK
    assert json.loads(result["body"]) is True

def test__delete_booking_controller__raises_domain_error(
    mocked_booking_deleter,
    seat_booking_factory
):
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()
    booking = seat_booking_factory(
        booking_id=booking_id,
        user_id=user_id
    )
    event = {"body":json.dumps({"user_id": user_id, "booking_id": booking_id})}

    mocked_booking_deleter(DomainError("Internal server error"))

    result = delete_booking_controller(event)

    assert result["status_code"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert result["body"] == '{"message": "Internal server error"}'

