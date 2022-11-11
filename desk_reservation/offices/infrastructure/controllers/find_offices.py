from http import HTTPStatus

from desk_reservation.shared.infrastructure.controllers.filters_controller import (
    filters_controller,
)

from desk_reservation.offices.application import OfficeFinder
from desk_reservation.shared.domain import DomainError
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    office_service_factory,
)
from desk_reservation.shared.infrastructure import (
    ControllerResponse,
    message_response,
)

# pylint: disable=W0613
def find_offices_controller(event, context=None, callback=None):
    office_service = office_service_factory()
    office_finder = OfficeFinder(office_service)
    params = event.get("queryStringParameters")
    populate = params.get("populate", False) if params else False
    criteria = filters_controller(params, False)
    try:
        result = office_finder.execute(criteria, populate)
        return ControllerResponse(
            HTTPStatus.OK, [ob.__dict__ for ob in result]
        ).__dict__
    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__
