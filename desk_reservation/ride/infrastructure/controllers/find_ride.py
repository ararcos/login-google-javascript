from http import HTTPStatus

from ...application import RideFinder
from ....shared.domain.exceptions import DomainError
from ....shared.infrastructure.dependency_injection import ride_service_factory
from ....shared.infrastructure import (
    ControllerResponse,
    Criteria,
    Filter,
    Operator,
    message_response,
)


def find_ride_controller(event):
    ride_service = ride_service_factory()
    ride_finder = RideFinder(ride_service)
    filters = [Filter(field="deleted_at", operator=Operator.EQUAL, value=None)]
    criteria = Criteria(filters=filters)
    try:
        result = ride_finder.execute(criteria=criteria)
        return ControllerResponse(status_code=HTTPStatus.OK, body=result).__dict__

    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__
