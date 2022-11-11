from http import HTTPStatus
import json
from pydantic import ValidationError
from desk_reservation.shared.domain.exceptions import DomainError, BadRequestError
from desk_reservation.shared.infrastructure.dependency_injection import ride_service_factory
from desk_reservation.shared.infrastructure import ControllerResponse, message_response
from desk_reservation.ride.application import RideBookingCreator
from desk_reservation.ride.domain import RideBooking


def create_ride_booking_controller(event, context=None, callback=None):
    try:
        ride_service = ride_service_factory()
        body = json.loads(event["body"])
        extra_seats = body.pop('extra_seats')
        ride_booking = RideBooking(**body)
        ride_booking_creator = RideBookingCreator(ride_service)
        result = ride_booking_creator.execute(
            extra_seats=extra_seats,
            ride_booking=ride_booking)
        response = (HTTPStatus.CREATED, result.__dict__) if result else (
            HTTPStatus.NOT_FOUND, {"message": "Ride not found"})
        return ControllerResponse(
            status_code=response[0],
            body=response[1]
        ).__dict__

    except (ValidationError, KeyError):
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body={"message": "Check Ride Attributes"}
        ).__dict__

    except BadRequestError as error :
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=response
        ).__dict__

    except DomainError as error:
        response = message_response(error.args)

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=response
        ).__dict__
