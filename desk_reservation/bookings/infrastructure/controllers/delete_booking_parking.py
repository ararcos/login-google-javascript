from http import HTTPStatus
import json

from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    booking_parking_service_factory,
)
from desk_reservation.bookings.application.booking_parking_deleter import (
    BookingParkingDeleter,
)
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse

# pylint: disable=W0613 R0801
def delete_booking_parking_controller(event, context=None, callback=None):
    booking_parking_service = booking_parking_service_factory()
    body = json.loads(event["body"])
    user_id = body.pop("user_id")
    booking_id = body.pop("booking_id")
    booking_deleter = BookingParkingDeleter(booking_parking_service)

    try:
        result = booking_deleter.execute(booking_id=booking_id, user_id=user_id)
        return ControllerResponse(status_code=HTTPStatus.OK, body=result).__dict__

    except IdNotFoundError as err:
        response = message_response(err.args)
        return ControllerResponse(
            status_code=HTTPStatus.NOT_FOUND, body=response
        ).__dict__

    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__
