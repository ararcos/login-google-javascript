from http import HTTPStatus

from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    lock_booking_service_factory,
)
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.shared.infrastructure.controllers import filters_controller
from desk_reservation.bookings.application import LockFinder

# pylint: disable=R0801 W0613
def find_lock_controller(event, context=None, callback=None):
    lock_service = lock_booking_service_factory()
    lock_finder = LockFinder(lock_service)
    params = event.get("queryStringParameters")
    try:
        criteria = filters_controller(params)
        result = lock_finder.execute(criteria)
        return ControllerResponse(
            HTTPStatus.OK, [ob.__dict__ for ob in result]
        ).__dict__

    except DomainError as err:
        response = message_response(err.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__
