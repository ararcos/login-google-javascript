import json
import pytest
from typing import Callable
from http import HTTPStatus
from faker import Faker
from desk_reservation.bookings.application.booking_getter import BookingGetter
from desk_reservation.bookings.infrastructure.controllers.get_booking import get_booking_controller
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError

@pytest.fixture(name='mocked_booking_getter')
def _mocked_library(mocker) -> Callable:
    def _create_booking_getter(booking_getter: any) -> None:
        mocker.patch('desk_reservation.bookings.infrastructure.controllers.get_booking.booking_service_factory',
                     return_value=mocker.Mock())
        mocker.patch.object(BookingGetter, 'execute',
                            side_effect=booking_getter)
    return _create_booking_getter

def test__get_booking_controller__return_booking(
    mocked_booking_getter,
    mocker,
    seat_booking_factory
):
    booking_id = Faker().uuid4()
    booking = seat_booking_factory(booking_id=booking_id)
    mocked_booking_getter(mocker.Mock(return_value=booking))
    event={'pathParameters':{"booking_id":booking_id}}
    result = get_booking_controller(event)

    assert result['status_code'] == HTTPStatus.CREATED
    assert result['body'] == json.dumps(booking.__dict__, default=str)

def test__get_booking_controller__raises_id_not_found_error(
        mocked_booking_getter,
        seat_booking_factory
):
    booking_id = Faker().uuid4()
    booking = seat_booking_factory(booking_id=booking_id)
    mocked_booking_getter(IdNotFoundError("Booking not found", booking_id))
    event={'pathParameters':{"booking_id":booking_id}}
    
    result = get_booking_controller(event)

    assert result['status_code'] == HTTPStatus.NOT_FOUND
    assert result['body'] == json.dumps({'message': "Booking not found id:'"+ booking_id +"' not found"})

def test__get_booking_controller__raises_domain_error(
        mocked_booking_getter,
        seat_booking_factory
):
    booking_id =  Faker().uuid4()
    booking = seat_booking_factory(booking_id=booking_id)
    mocked_booking_getter(DomainError("Internal error"))

    event={'pathParameters':{"booking_id":booking_id}}
    
    result = get_booking_controller(event)

    assert result["status_code"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert result['body'] == json.dumps({'message': "Internal error"})