from http import HTTPStatus

from desk_reservation.shared.infrastructure.controllers.filters_controller import filters_controller

from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.seats.application.seat_finder import SeatFinder
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.infrastructure.controllers.controller_response import (
    ControllerResponse
    )
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    seat_service_factory
    )

# pylint: disable=W0613
def find_seat_controller(event, context=None, callback=None):
    seat_service = seat_service_factory()
    seats_finder = SeatFinder(seat_service)
    params = event.get('queryStringParameters')
    try:
        criteria = filters_controller(params,False)
        result = seats_finder.execute(criteria)
        return ControllerResponse(HTTPStatus.OK, [ob.__dict__ for ob in result]).__dict__
    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response).__dict__
