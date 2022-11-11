from http import HTTPStatus

from desk_reservation.shared.infrastructure.controllers.filters_controller import (
    filters_controller,
)

from desk_reservation.parkings.application.parking_finder import ParkingFinder
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.infrastructure.controllers.controller_response import ControllerResponse
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    parking_service_factory,
)


def find_parking_controller(event, context=None, callback=None):
    parking_service = parking_service_factory()
    parkings_finder = ParkingFinder(parking_service)
    params = event.get("queryStringParameters")
    try:
        criteria = filters_controller(params,False)
        result = parkings_finder.execute(criteria)
        return ControllerResponse(HTTPStatus.OK, [ob.__dict__ for ob in result]).__dict__

    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__
