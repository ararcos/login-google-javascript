from http import HTTPStatus
from pydantic import ValidationError

from ....shared.domain.exceptions import NameAlreadyExistsError
from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.controllers import message_response
from ...application.seat_updater import SeatUpdater
from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.domain.exceptions.id_not_found_error import IdNotFoundError
from ....shared.infrastructure.dependency_injection.services_factory import seat_service_factory
from ....shared.infrastructure.controllers import ControllerResponse
from ...domain import Seat


def update_seat_controller(event):
    seat_service = seat_service_factory()
    user_id = event.pop('user_id')
    try:
        edited_seat = Seat(**event['seat'])
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
