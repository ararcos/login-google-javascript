from http import HTTPStatus
import json
from pydantic import ValidationError

from desk_reservation.shared.domain.exceptions import NameAlreadyExistsError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    seat_service_factory,
)
from desk_reservation.shared.infrastructure.controllers import ControllerResponse
from desk_reservation.seats.application import SeatCreator
from desk_reservation.seats.domain import Seat

# pylint: disable= R0801 W0613
def create_seat_controller(event, context=None, callback=None):
    seat_service = seat_service_factory()
    try:
        body = json.loads(event["body"])
        user_id = body.pop("user_id")
        seat = Seat(**body)
        seat_creator = SeatCreator(seat_service)
        result = seat_creator.execute(seat=seat, user_id=user_id)
        return ControllerResponse(
            status_code=HTTPStatus.CREATED,
            body=result.__dict__
        ).__dict__

    except ValidationError:
        return ControllerResponse(
            status_code=HTTPStatus.CONFLICT,
            body={"message": "Check seat attributes"}
        ).__dict__

    except NameAlreadyExistsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.CONFLICT, body=response
        ).__dict__

    except PermissionsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.UNAUTHORIZED, body=response
        ).__dict__

    except DomainError as error:
        response = {"message": error.args[0]}
        if len(error.args) == 2:
            response["details"] = error.args[1]
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=response
        ).__dict__
