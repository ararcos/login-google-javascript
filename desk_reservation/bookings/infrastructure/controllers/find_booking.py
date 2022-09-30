from http import HTTPStatus
import json

from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import booking_service_factory
from desk_reservation.shared.infrastructure.firestore.firestore_criteria.criteria import Criteria
from desk_reservation.shared.infrastructure.firestore.firestore_criteria.filter import Filter
from desk_reservation.shared.infrastructure.firestore.firestore_criteria.operator import Operator
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.bookings.application import BookingFinder

def find_booking_controller(event, context=None, callback=None):
    return ControllerResponse(
        status_code=HTTPStatus.CREATED,
        body=event).__dict__
    # booking_service = booking_service_factory()
    # booking_finder = BookingFinder(booking_service)
    # filters = [
    #     Filter(field=_key, operator=Operator.EQUAL, value=_value)
    #     for _key, _value in json.loads(event['filters']).items()
    # ]
    # criteria = Criteria(filters)
    # try:
    #     result = booking_finder.execute(criteria)
    #     return ControllerResponse(HTTPStatus.OK, result).__dict__

    # except DomainError as err:
    #     response = message_response(err.args)
    #     return ControllerResponse(
    #         status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
    #     ).__dict__
