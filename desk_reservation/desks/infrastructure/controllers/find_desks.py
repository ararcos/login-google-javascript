from http import HTTPStatus
from http.client import OK


from ...application.desk_finder import DeskFinder
from ....shared.infrastructure.controllers import ControllerResponse
from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.infrastructure.firestore.firestore_criteria.filter import Filter
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ....shared.infrastructure.firestore.firestore_criteria.operator import Operator
from ....shared.infrastructure.dependency_injection.services_factory import desk_service_factory
from ....shared.infrastructure.controllers.message_response import message_response

# pylint:disable=duplicate-code
def find_desks_controller():
    desk_service = desk_service_factory()
    desk_finder = DeskFinder(desk_service)
    filters = [Filter(field='deleted_at', operator=Operator.EQUAL, value=None)]
    criteria = Criteria(filters=filters)
    try:
        result = desk_finder.execute(criteria)
        return ControllerResponse(OK, result).__dict__

    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            body=response
        ).__dict__
    