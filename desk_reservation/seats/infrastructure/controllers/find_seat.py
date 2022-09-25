from http import HTTPStatus

from ....shared.infrastructure.controllers import message_response
from ...application.seat_finder import SeatFinder
from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.infrastructure.controllers.controller_response import ControllerResponse
from ....shared.infrastructure.dependency_injection.services_factory import seat_service_factory
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ....shared.infrastructure.firestore.firestore_criteria.filter import Filter
from ....shared.infrastructure.firestore.firestore_criteria.operator import Operator


def find_seat_controller():
    seat_service = seat_service_factory()
    seats_finder = SeatFinder(seat_service)
    filters = [Filter(field='deleted_at', operator=Operator.EQUAL, value=None)]
    criteria = Criteria(filters)
    try:
        result = seats_finder.execute(criteria)
        return ControllerResponse(HTTPStatus.OK, result).__dict__
    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response).__dict__
