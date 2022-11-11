import json
from http import HTTPStatus

from desk_reservation.bookings.application import LockCreator
from desk_reservation.bookings.domain.entities import LockBooking
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    lock_booking_service_factory,
)


# pylint: disable= R0801 W0613 W0703
def create_lock_controller(event, context=None, callback=None):
    try:
        lock_service = lock_booking_service_factory()
        lock_booking = LockBooking(**json.loads(event["body"]))
        lock_creator = LockCreator(lock_service)
        result = lock_creator.execute(lock_booking)
        return ControllerResponse(
            status_code=HTTPStatus.CREATED, body=result.__dict__
        ).__dict__
    except DomainError as error:
        response = {"message": error.args[0]}
        if len(error.args) == 2:
            response["details"] = error.args[1]

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=response
        ).__dict__
    except Exception as error:
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=str(error)
        ).__dict__
