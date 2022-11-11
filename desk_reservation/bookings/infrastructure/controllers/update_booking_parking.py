from http import HTTPStatus
import json

from pydantic import ValidationError
from desk_reservation.bookings.application.booking_parking_updater import BookingParkingUpdater
from desk_reservation.bookings.domain.entities.booking import ParkingBooking
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    booking_parking_service_factory,
)
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.shared.domain.exceptions import IdNotFoundError

# pylint: disable=R0801 W0613 W0703
def update_booking_parking_controller(event, context=None, callback=None):
    try:
        booking_parking_service = booking_parking_service_factory()
        body = json.loads(event["body"])
        booking_id = body['booking_id']
        user_id = body.pop('user_id')
        edited_booking = ParkingBooking(**body)
        booking_updater = BookingParkingUpdater(booking_parking_service)
        result = booking_updater.execute(
            booking_id=booking_id, user_id=user_id, booking=edited_booking
        )
        response = (
            (HTTPStatus.OK, result.__dict__) if result else (HTTPStatus.NOT_FOUND, None)
        )
        return ControllerResponse(status_code=response[0], body=response[1]).__dict__

    except (ValidationError, KeyError) as error:
        print(error)
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body={"message": "Check Booking Attributes"},
        ).__dict__

    except IdNotFoundError as error:
        response = {"message": error.args[0]}
        if len(error.args) == 2:
            response["details"] = error.args[1]
        return ControllerResponse(
            status_code=HTTPStatus.NOT_FOUND, body=response
        ).__dict__

    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__

    except Exception as error:
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=str(error)
        ).__dict__