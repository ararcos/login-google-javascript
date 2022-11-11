from http import HTTPStatus

from desk_reservation.ride.application import RideFinder
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.dependency_injection import ride_service_factory
from desk_reservation.shared.infrastructure.controllers import filters_controller
from desk_reservation.shared.infrastructure import (
    ControllerResponse,
    Criteria,
    Filter,
    Operator,
    message_response,
)


def find_ride_controller(event, context=None, callback=None):
    ride_service = ride_service_factory()
    ride_finder = RideFinder(ride_service)
    params = event.get('queryStringParameters')
    try:
        criteria = filters_controller(params)
        result = ride_finder.execute(criteria)
        return ControllerResponse(HTTPStatus.OK, [ob.__dict__ for ob in result]).__dict__

    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__
