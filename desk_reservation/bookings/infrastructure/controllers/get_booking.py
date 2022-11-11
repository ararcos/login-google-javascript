from http import HTTPStatus

from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    booking_service_factory,
)
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.shared.domain.exceptions import IdNotFoundError
from desk_reservation.bookings.application import BookingGetter

# pylint: disable= R0801 W0613 W0703
def get_booking_controller(event, context=None, callback=None):
    booking_service = booking_service_factory()
    booking_id = event["pathParameters"]["booking_id"]
    booking_getter = BookingGetter(booking_service)

    try:
        result = booking_getter.execute(booking_id=booking_id)
        return ControllerResponse(
            status_code=HTTPStatus.CREATED,
            body=result.__dict__
        ).__dict__

    except IdNotFoundError as error:
        response = message_response(error.args)
        return ControllerResponse(
        status_code=HTTPStatus.NOT_FOUND, body=response).__dict__

    except DomainError as error:
        response = {
            'message': error.args[0]
        }
        if len(error.args) == 2:
            response['details'] = error.args[1]
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            body=response
        ).__dict__
    except Exception as error:
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=str(error)
        ).__dict__
