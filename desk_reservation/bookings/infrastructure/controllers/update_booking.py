from http import HTTPStatus
import json
from pydantic import ValidationError
from desk_reservation.bookings.domain.entities import Booking
from desk_reservation.bookings.application import BookingUpdater
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import booking_service_factory
from desk_reservation.shared.domain.exceptions import DomainError
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.shared.domain.exceptions import IdNotFoundError

def update_booking_controller(event, context=None, callback=None):
    try:
        booking_service = booking_service_factory()
        booking_id = json.loads(event["body"]).pop('booking_id')
        user_id = json.loads(event["body"]).pop('user_id')
        edited_booking = Booking(**json.loads(event["body"]['booking']))
        booking_updater = BookingUpdater(booking_service)
        result = booking_updater.execute(
                booking_id=booking_id,
                user_id=user_id,
                booking=edited_booking
        )
        ##TODO return has_pet and has_child info too
        ##Validate "booking_id" value from "updated_booking" has the same value of "booking_id" in the event
        response = (HTTPStatus.OK, result.__dict__) if result else( HTTPStatus.NOT_FOUND, None)
        return ControllerResponse(
            status_code=response[0],
            body=json.dumps(response[1], default = str)
        ).__dict__

    except (ValidationError, KeyError) :
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body={"message": "Check Booking Attributes"}
        ).__dict__

    except IdNotFoundError as error:
        response = {
            'message': error.args[0]
        }
        if len(error.args) == 2:
            response['details'] = error.args[1]
        return ControllerResponse(
        status_code=HTTPStatus.NOT_FOUND, body=json.dumps(response)).__dict__

    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, body=response
        ).__dict__

    except Exception as error:
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=str(error)
        ).__dict__
