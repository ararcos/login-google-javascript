from http import HTTPStatus
import json
from pydantic import ValidationError

from desk_reservation.seats.domain.entities.seat import Seat
from desk_reservation.seats.application.seat_updater import SeatUpdater
from desk_reservation.shared.domain.exceptions import NameAlreadyExistsError
from desk_reservation.shared.domain.exceptions.permissions_error import PermissionsError
from desk_reservation.shared.infrastructure.controllers import message_response
from desk_reservation.shared.domain.exceptions.domain_error import DomainError
from desk_reservation.shared.domain.exceptions.id_not_found_error import IdNotFoundError
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    seat_service_factory)
from desk_reservation.shared.infrastructure.controllers import ControllerResponse


# pylint: disable=W0613
def update_seat_controller(event, context=None, callback=None):
    seat_service = seat_service_factory()
    try:
        body = json.loads(event["body"])
        user_id = body.pop('user_id')
        edited_seat = Seat(**body)
        seat_editor = SeatUpdater(seat_service)
        result = seat_editor.execute(user_id=user_id, seat=edited_seat)
        return ControllerResponse(
            status_code=HTTPStatus.OK,
            body=result.__dict__
        ).__dict__

    except PermissionsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.UNAUTHORIZED, body=response).__dict__

    except NameAlreadyExistsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.CONFLICT, body=response).__dict__

    except IdNotFoundError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.NOT_FOUND, body=response).__dict__

    except ValidationError:
        return ControllerResponse(
            status_code=HTTPStatus.CONFLICT, body={'message': "Check seat attributes"}).__dict__

    except DomainError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=response).__dict__
