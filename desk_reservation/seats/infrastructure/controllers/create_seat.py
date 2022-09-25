from http import HTTPStatus
from pydantic import ValidationError

from ....shared.domain.exceptions import NameAlreadyExistsError
from ....shared.domain.exceptions.permissions_error import PermissionsError
from ....shared.infrastructure.controllers import message_response
from ....shared.domain.exceptions.domain_error import DomainError
from ....shared.infrastructure.dependency_injection.services_factory import seat_service_factory
from ....shared.infrastructure.controllers import ControllerResponse
from ...application import SeatCreator
from ...domain import Seat


def create_seat_controller(event):
    seat_service = seat_service_factory()
    user_id = event.pop('user_id')
    try:
        seat = Seat(**event['seat'])
        seat_creator = SeatCreator(seat_service)
        result = seat_creator.execute(seat=seat, user_id=user_id)
        return ControllerResponse(
            status_code=HTTPStatus.CREATED, body=result.__dict__).__dict__

    except ValidationError:
        return ControllerResponse(
            status_code=HTTPStatus.CONFLICT, body={'message': "Check seat attributes"}).__dict__

    except NameAlreadyExistsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.CONFLICT, body=response).__dict__

    except PermissionsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.UNAUTHORIZED, body=response).__dict__

    except DomainError as error:
        response = {'message': error.args[0]}
        if len(error.args) == 2:
            response['details'] = error.args[1]
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=response).__dict__
