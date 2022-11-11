import json
from http import HTTPStatus
from xml.dom import ValidationErr
from desk_reservation.bookings.application.booking_parking_creator import (
    BookingParkingCreator,
)
from desk_reservation.bookings.domain.entities.booking import ParkingBooking
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    booking_parking_service_factory,
)
# pylint: disable=W0613 W0703 R0801 W0311
def create_booking_parking_controller(event, context=None, callback=None):
    try:
        booking_parking_service = booking_parking_service_factory()
        booking = ParkingBooking(**json.loads(event["body"]))
        booking_parking_creator = BookingParkingCreator(booking_parking_service)
        result = booking_parking_creator.execute(booking)
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
    except (ValidationErr, KeyError) :
            return ControllerResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                body={"message": "Check booking Attributes"}
            ).__dict__
    except Exception as error:
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=str(error)
        ).__dict__
