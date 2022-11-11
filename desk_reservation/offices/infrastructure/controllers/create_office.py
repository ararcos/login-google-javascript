from http import HTTPStatus
import json

from pydantic import ValidationError

from desk_reservation.offices.domain import Office
from desk_reservation.offices.application import OfficeCreator
from desk_reservation.shared.domain.exceptions import PermissionsError, DomainError
from desk_reservation.shared.infrastructure import ControllerResponse, message_response
from desk_reservation.shared.infrastructure.dependency_injection.services_factory import (
    office_service_factory,
)

# pylint: disable=W0613, R0801
def create_office_controller(event, context=None, callback=None):
    office_service = office_service_factory()
    try:
        body = json.loads(event["body"])
        user_id = body.pop("user_id")
        office = Office(**body)
        office_creator = OfficeCreator(office_service)
        result = office_creator.execute(office=office, user_id=user_id)
        return ControllerResponse(status_code=HTTPStatus.CREATED, body=result).__dict__

    except PermissionsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.FORBIDDEN, body=response
        ).__dict__

    except (ValidationError, KeyError):
        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body={"message": "Check Desk Attributes"},
        ).__dict__

    except DomainError as error:
        response = message_response(error.args)

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST, body=response
        ).__dict__
