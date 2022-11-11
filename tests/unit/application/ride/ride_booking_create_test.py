import pytest

from desk_reservation.ride.application.ride_booking_create import RideBookingCreator
from desk_reservation.shared.domain.exceptions.bad_request import BadRequestError


def test__ride_booking_creator_return_ride_when_ride_booking_is_created_and_not_have_extra_seats(
        mocker, ride_factory, ride_booking_factory):

    ride_booking_to_save = ride_booking_factory()
    ride_bookings = [ride_booking_factory()]
    ride = ride_factory(passengers=ride_bookings, total_spots=4)
    ride_service = mocker.Mock(
        find_by_id=mocker.Mock(return_value=ride),
        booking_ride=mocker.Mock(return_value=ride_booking_to_save)
    )
    ride_booking_creator = RideBookingCreator(ride_service=ride_service)

    result = ride_booking_creator.execute(
        ride_booking=ride_booking_to_save, extra_seats=0)

    assert ride_service.find_by_id.calledWith(
        ride_id=ride_booking_to_save.ride_id)
    assert ride_service.booking_ride.calledWith(
        ride_booking=ride_booking_to_save)
    assert result.passengers == ride_bookings + [ride_booking_to_save]


def test__ride_booking_creator_return_ride_with_extra_seats_when_have_extra_seats(
        mocker, ride_factory, ride_booking_factory):

    ride_booking_to_save = ride_booking_factory(is_extra_seat=False)
    ride_bookings = [ride_booking_factory(is_extra_seat=False)]
    ride = ride_factory(passengers=ride_bookings, total_spots=4)
    ride_service = mocker.Mock(
        find_by_id=mocker.Mock(return_value=ride),
        booking_ride=mocker.Mock(return_value=ride_booking_to_save)
    )
    ride_booking_creator = RideBookingCreator(ride_service=ride_service)

    result = ride_booking_creator.execute(
        ride_booking=ride_booking_to_save, extra_seats=2)

    assert ride_service.find_by_id.calledWith(
        ride_id=ride_booking_to_save.ride_id)
    assert ride_service.booking_ride.call_count == 3
    assert len(result.passengers) == 4
    assert ride_booking_to_save in result.passengers


def test__ride_booking_creator_raise_bad_request_when_trying_to_book_more_seats_than_available(
        mocker, ride_factory, ride_booking_factory):

    ride_booking_to_save = ride_booking_factory()
    ride_bookings = [ride_booking_factory()]
    ride = ride_factory(passengers=ride_bookings, total_spots=2)
    ride_service = mocker.Mock(
        find_by_id=mocker.Mock(return_value=ride),
        booking_ride=mocker.Mock(return_value=ride_booking_to_save)
    )
    ride_booking_creator = RideBookingCreator(ride_service=ride_service)

    with pytest.raises(BadRequestError):
        ride_booking_creator.execute(
            ride_booking=ride_booking_to_save, extra_seats=2)
        assert ride_service.find_by_id.calledWith(
            ride_id=ride_booking_to_save.ride_id)
        assert ride_service.booking_ride.call_count == 0


def test__ride_booking_creator_return_none_when_booking_in_a_ride_that_does_not_exist(
        mocker, ride_booking_factory):

    ride_booking_to_save = ride_booking_factory()
    ride_service = mocker.Mock(
        find_by_id=mocker.Mock(return_value=None),
        booking_ride=mocker.Mock(return_value=ride_booking_to_save)
    )
    ride_booking_creator = RideBookingCreator(ride_service=ride_service)

    result = ride_booking_creator.execute(
        ride_booking=ride_booking_to_save, extra_seats=2)
    assert ride_service.booking_ride.call_count == 0
    assert ride_service.find_by_id.calledWith(
        ride_id=ride_booking_to_save.ride_id)
    assert result is None
