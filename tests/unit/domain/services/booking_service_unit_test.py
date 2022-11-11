from datetime import datetime
from faker import Faker
import pytest

from desk_reservation.bookings.domain.exceptions import UserAlreadyHasReservation
from desk_reservation.bookings.domain.exceptions.invalid_date_range_error import InvalidDateRange
from desk_reservation.bookings.domain.services import BookingService
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError


@pytest.fixture(name='dependencies')
def _service_dependencies(mocker):
    booking_repository = mocker.Mock()
    user_repository = mocker.Mock()
    seat_repository = mocker.Mock()
    office_repository = mocker.Mock()
    booking_service = BookingService(
        booking_repository=booking_repository, 
        user_repository=user_repository,
        seat_repository=seat_repository,
        office_repository=office_repository
    )
    return {
        'booking_repository': booking_repository,
        'user_repository': user_repository,
        'service': booking_service,
    }


def test__create_booking__was_called_correctly(dependencies, mocker, seat_booking_factory):
    booking_repository, __user_repository, service = dependencies.values()
    booking = seat_booking_factory()

    service.dates_booking_validator = mocker.Mock(return_value=True)
    service.user_reservations_by_dates = mocker.Mock(return_value=[])

    service.create_booking(booking)

    booking_repository.create.assert_called_with(booking)

def test__create_booking__raise_already_reservation_exception(
    dependencies, mocker, seat_booking_factory):
    __booking_repository, __user_repository, service = dependencies.values()
    service.dates_booking_validator = mocker.Mock(return_value=None)
    service.user_reservations_by_dates = mocker.Mock(return_value=[mocker.Mock()])
    booking = seat_booking_factory()

    with pytest.raises(UserAlreadyHasReservation):
        service.create_booking(booking)

def test__create_bookings__was_called_correctly(dependencies, mocker, seat_booking_factory):
    booking_repository, __user_repository, service = dependencies.values()
    service.dates_booking_validator = mocker.Mock(return_value=[mocker.Mock()])
    service.user_reservations_by_dates = mocker.Mock(return_value=[])

    booking = seat_booking_factory()
    booking1 = seat_booking_factory()
    bookings = [booking, booking1]

    service.create_bookings(bookings)

    booking_repository.create_many.assert_called_with(bookings)

def test__create_bookings__raise_already_reservation_exception(
    dependencies, mocker, seat_booking_factory):
    __booking_repository, __user_repository, service = dependencies.values()
    service.dates_booking_validator = mocker.Mock(return_value=[mocker.Mock()])
    service.user_reservations_by_dates = mocker.Mock(return_value=[mocker.Mock()])

    booking = seat_booking_factory()
    booking1 = seat_booking_factory()
    bookings = [booking, booking1]

    with pytest.raises(UserAlreadyHasReservation):
        service.create_bookings(bookings)

def test__get_booking_by_id__was_called_correctly(dependencies, mocker, seat_booking_factory):
    booking_repository, __user_repository, service = dependencies.values()
    booking_id = Faker().uuid4()
    booking = seat_booking_factory(booking_id=booking_id)

    booking_repository.get = mocker.Mock(return_value=booking)

    result = service.get_booking_by_id(booking_id)

    assert result == booking

def test__get_booking_by_id__was_called_when_id_is_not_found(dependencies, mocker):
    booking_repository, __user_repository, service = dependencies.values()
    booking_id = Faker().uuid4()

    booking_repository.get = mocker.Mock(return_value=None)

    with pytest.raises(IdNotFoundError):
        service.get_booking_by_id(booking_id)

def test__find_bookings__was_called_correctly(dependencies, mocker):
    booking_repository, __user_repository, service = dependencies.values()
    criteria = mocker.Mock()

    service.find_bookings(criteria, populate=False)

    booking_repository.find.assert_called_with(criteria)

def test__update_booking__was_called_correctly(dependencies, mocker, seat_booking_factory):
    booking_repository, __user_repository, service = dependencies.values()
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()
    booking = seat_booking_factory(booking_id=booking_id)
    booking_repository.update = mocker.Mock(return_value=booking)

    result = service.update_booking(
        booking_id=booking_id,
        user_id=user_id,
        booking=booking
        )

    assert result == booking

def test__update_booking__was_called_when_id_is_not_found(
        dependencies,
        mocker,
        seat_booking_factory
    ):
    booking_repository, __user_repository, service = dependencies.values()
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()
    booking = seat_booking_factory(booking_id=booking_id)
    booking_repository.update = mocker.Mock(return_value=None)

    with pytest.raises(IdNotFoundError):
        service.update_booking(
            booking_id=booking_id,
            user_id=user_id,
            booking=booking
        )

def test__delete_booking__was_called_correctly(dependencies, mocker):
    booking_repository, __user_repository, service = dependencies.values()
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()

    booking_repository.delete = mocker.Mock(return_value=True)

    result = service.delete_booking(booking_id, user_id)

    assert result is True

def test__delete_booking__was_called_when_id_is_not_found(dependencies, mocker):
    booking_repository, __user_repository, service = dependencies.values()
    booking_id = Faker().uuid4()
    user_id = Faker().uuid4()

    booking_repository.delete = mocker.Mock(return_value=False)

    with pytest.raises(IdNotFoundError):
        service.delete_booking(booking_id, user_id)

def test__booking_can_be_edited__booked_date_end_is_minor_than_actual_date(
        dependencies,
        mocker,
        user_factory,
        seat_booking_factory
    ):
    __booking_repository, user_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    user = user_factory(google_id=user_id)
    user_repository.get = mocker.Mock(return_value=user)
    date_earlier_than_today = Faker().past_datetime()
    booking = seat_booking_factory(booked_date_end=date_earlier_than_today)

    result = service.booking_can_be_edited(booking=booking, user_id=user_id)

    assert result is False

def test__booking_can_be_edited__when_return_true(
        dependencies,
        mocker,
        user_factory,
        seat_booking_factory
    ):
    __booking_repository, user_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    user = user_factory(google_id=user_id, admin=True)
    user_repository.get = mocker.Mock(return_value=user)
    date_later_than_today = Faker().future_datetime()

    booking = seat_booking_factory(booked_date_end=date_later_than_today)

    result = service.booking_can_be_edited(booking=booking, user_id=user_id)

    assert result is True

def test__booking_can_be_edited__when_return_false(
        dependencies,
        mocker,
        user_factory,
        seat_booking_factory
    ):
    __booking_repository, user_repository, service = dependencies.values()
    user_id = Faker().uuid4()
    user = user_factory(google_id=user_id, admin=False)
    user_repository.get = mocker.Mock(return_value=user)
    date_later_than_today = Faker().future_datetime()

    booking = seat_booking_factory(booked_date_end=date_later_than_today)

    result = service.booking_can_be_edited(booking=booking, user_id=user_id)

    assert result is False

def test__user_reservations_by_dates__was_called_correctly(dependencies, mocker):
    __booking_repository, __user_repository, service = dependencies.values()
    criteria = mocker.Mock()
    user_id = Faker().uuid4()
    date_init = datetime.today()
    date_end = Faker().future_date()
    bookings = [mocker.Mock()]

    service.user_reservations_by_dates(
            date_init=date_init,
            date_end=date_end,
            user_id=user_id
        )

    service.find_bookings = mocker.Mock(return_value=bookings)

    assert service.find_bookings(criteria) == bookings

def test__dates_booking_validator__invalid_date_range__different_days(
        dependencies,
        seat_booking_factory
    ):
    __booking_repository, __user_repository, service = dependencies.values()
    date_init = Faker().past_datetime()
    date_end = Faker().future_datetime()

    booking = seat_booking_factory(
            booked_date_init=date_init,
            booked_date_end=date_end
        )

    with pytest.raises(InvalidDateRange):
        service.dates_booking_validator(booking=booking)

def test__dates_booking_validator__invalid_date_range__book_in_past(
        dependencies,
        seat_booking_factory
    ):
    __booking_repository, __user_repository, service = dependencies.values()
    date_init = Faker().past_datetime()

    booking = seat_booking_factory(booked_date_init=date_init)

    with pytest.raises(InvalidDateRange):
        service.dates_booking_validator(booking=booking)

def test__dates_booking_validator__return_true(dependencies,seat_booking_factory):
    __booking_repository, __user_repository, service = dependencies.values()
    date_init = datetime.today()
    date_end = datetime.today()

    booking = seat_booking_factory(
            booked_date_init=date_init,
            booked_date_end=date_end
        )

    result = service.dates_booking_validator(booking)

    assert result is True
