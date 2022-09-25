from http import HTTPStatus

from ...application import OfficeDeleter
from ....shared.domain.exceptions import PermissionsError
from ....shared.infrastructure import ControllerResponse
from ....shared.infrastructure.dependency_injection.services_factory import office_service_factory


def delete_office_controller(event):
    office_service = office_service_factory()
    office_deleter = OfficeDeleter(office_service)

    try:
        result = office_deleter.execute(
            office_id=event['office_id'], user_id=event['user_id'])
        status_code = HTTPStatus.OK if result else HTTPStatus.NOT_FOUND
        return ControllerResponse(
            status_code=status_code,
            body=None
        ).__dict__

    except PermissionsError as error:
        return ControllerResponse(
            status_code=HTTPStatus.FORBIDDEN,
            body={'message': error.args[0]}
        ).__dict__
