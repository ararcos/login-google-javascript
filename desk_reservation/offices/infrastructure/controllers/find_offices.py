
from http import HTTPStatus

from ...application import OfficeFinder
from ....shared.domain import DomainError
from ....shared.infrastructure.dependency_injection.services_factory import office_service_factory
from ....shared.infrastructure import (ControllerResponse, Filter, Operator, Criteria,
                                       message_response)


def find_offices_controller():
    office_service = office_service_factory()
    office_finder = OfficeFinder(office_service)
    filters = [Filter(field='deleted_at', operator=Operator.EQUAL, value=None)]
    criteria = Criteria(filters=filters)
    try:
        result = office_finder.execute(criteria)
        return ControllerResponse(HTTPStatus.OK, result).__dict__
    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            body=response
        ).__dict__
