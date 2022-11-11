from http import HTTPStatus

from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    booking_service_factory,
)
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.bookings.application import BookingFinder
from desk_reservation.shared.infrastructure.controllers import filters_controller

# pylint: disable=W0613
def find_booking_controller(event, context=None, callback=None):
    booking_service = booking_service_factory()
    booking_finder = BookingFinder(booking_service)
    params = event.get("queryStringParameters")
    populate = params.get("populate", False) if params else False
    try:
        criteria = filters_controller(params)
        result = booking_finder.execute(criteria, populate)
        return ControllerResponse(
            HTTPStatus.OK, [ob.__dict__ for ob in result]
        ).__dict__

    except DomainError as err:
        response = message_response(err.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__
