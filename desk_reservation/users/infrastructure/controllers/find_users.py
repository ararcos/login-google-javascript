from http import HTTPStatus
#pylint: disable=R0801

from ....shared.infrastructure.controllers import message_response
from ....shared.infrastructure.controllers import ControllerResponse
from ....shared.infrastructure.dependency_injection import user_service_factory
from ....shared.infrastructure.firestore.firestore_criteria import Criteria
from ....shared.infrastructure.firestore.firestore_criteria import Operator
from ...application.user_finder import UserFinder
from ....shared.infrastructure.firestore.firestore_criteria.filter import Filter
from ....shared.domain.exceptions.domain_error import DomainError


def find_users_controller():
    user_service = user_service_factory()
    user_finder = UserFinder(user_service)
    filters = [Filter(field='deleted_at', operator=Operator.EQUAL, value=None)]
    criteria = Criteria(filters=filters)
    try:
        result = user_finder.execute(criteria)
        return ControllerResponse(HTTPStatus.OK, result).__dict__
    except DomainError as error:
        response = message_response(error.args)

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=response
        ).__dict__
