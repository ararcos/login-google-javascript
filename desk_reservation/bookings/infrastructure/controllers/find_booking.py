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
from desk_reservation.shared.infrastructure.controllers import filters_controller

def find_booking_controller(event, context):
    booking_service = booking_service_factory()
    booking_finder = BookingFinder(booking_service)
    params = event.get('queryStringParameters')
    try:
        criteria = filters_controller(params)
        result = booking_finder.execute(criteria)
        return ControllerResponse(HTTPStatus.OK, [ob.__dict__ for ob in result]).__dict__

    except DomainError as err:
        response = message_response(err.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__
