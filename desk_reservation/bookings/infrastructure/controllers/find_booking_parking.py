from http import HTTPStatus

from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.shared.infrastructure.controllers import filters_controller
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    booking_parking_service_factory,
)
from desk_reservation.bookings.application.booking_parking_finder import (
    BookingParkingFinder,
)

# pylint: disable=R0801 W0613
def find_booking_parking_controller(event, context=None, callback=None):
    booking_parking_service = booking_parking_service_factory()
    booking_finder = BookingParkingFinder(booking_parking_service)
    params = event.get("queryStringParameters")
    try:
        criteria = filters_controller(params)
        result = booking_finder.execute(criteria)
        return ControllerResponse(
            HTTPStatus.OK, [ob.__dict__ for ob in result]
        ).__dict__

    except DomainError as err:
        response = message_response(err.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__
