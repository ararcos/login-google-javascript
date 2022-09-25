from http import HTTPStatus

from ...domain import Office
from ...application import OfficeCreator
from ....shared.domain.exceptions import PermissionsError, DomainError
from ....shared.infrastructure import ControllerResponse, message_response
from ....shared.infrastructure.dependency_injection.services_factory import office_service_factory


def create_office_controller(event):
    office_service = office_service_factory()
    user_id = event.pop('user_id')
    office = Office(**event)
    office_creator = OfficeCreator(office_service)
    try:
        result = office_creator.execute(
            office=office, user_id=user_id).__dict__
        return ControllerResponse(
            status_code=HTTPStatus.CREATED,
            body=result
        ).__dict__

    except PermissionsError as error:
        response = message_response(error.args)
        return ControllerResponse(
            status_code=HTTPStatus.FORBIDDEN,
            body=response
        ).__dict__

    except DomainError as error:
        response = message_response(error.args)

        return ControllerResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body=response
        ).__dict__
