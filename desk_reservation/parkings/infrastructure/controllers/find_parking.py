from http import HTTPStatus

from ...application.parking_finder import ParkingFinder
from ....shared.infrastructure.controllers import message_response
from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.infrastructure.controllers.controller_response import ControllerResponse
from ....shared.infrastructure.dependency_injection.services_factory import parking_service_factory
from ....shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from ....shared.infrastructure.firestore.firestore_criteria.filter import Filter
from ....shared.infrastructure.firestore.firestore_criteria.operator import Operator


def find_parking_controller():
    parking_service = parking_service_factory()
    parkings_finder = ParkingFinder(parking_service)
    filters = [Filter(field='deleted_at', operator=Operator.EQUAL, value=None)]
    criteria = Criteria(filters)
    try:
        result = parkings_finder.execute(criteria)
        return ControllerResponse(HTTPStatus.OK, result).__dict__
    
    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response).__dict__
