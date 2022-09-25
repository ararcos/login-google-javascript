from http import HTTPStatus

from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError

from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import booking_service_factory
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.bookings.application import BookingDeleter

def delete_booking_controller(event, context=None, callback=None):
    booking_service = booking_service_factory()
    user_id = event.pop('user_id')
    booking_id = event.pop('booking_id')
    booking_deleter = BookingDeleter(booking_service)

    try:
        result = booking_deleter.execute(
            booking_id=booking_id,
            user_id=user_id
        )
        return ControllerResponse(
            status_code=HTTPStatus.OK,
            body=result).__dict__

    except IdNotFoundError as err:
        response = message_response(err.args)
        return ControllerResponse(status_code=HTTPStatus.NOT_FOUND, body=response).__dict__

    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__
