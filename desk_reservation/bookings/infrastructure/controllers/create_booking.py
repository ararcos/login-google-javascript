import json
from http import HTTPStatus

from desk_reservation.bookings.application import BookingCreator
from desk_reservation.bookings.domain.entities import SeatBooking
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import booking_service_factory


# pylint: disable=W0613
def create_book(event, context=None, callback=None):
    try:
        booking_service = booking_service_factory()
        booking = SeatBooking(**event["body"])
        booking_creator = BookingCreator(booking_service)
        result = booking_creator.execute(booking)
        return ControllerResponse(
            status_code=HTTPStatus.CREATED,
            body=json.dumps(result.__dict__, default=str)
        ).__dict__
    except DomainError as error:
        response = {
            'message': error.args[0]
        }
        if len(error.args) == 2:
            response['details'] = error.args[1]

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=response
        ).__dict__
    except Exception as error:
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=str(error)
        ).__dict__
        