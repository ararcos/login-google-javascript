from http import HTTPStatus

from ...domain import Office
from ...application import OfficeUpdater
from ....shared.domain.exceptions import PermissionsError
from ....shared.infrastructure.dependency_injection.services_factory import office_service_factory
from ....shared.infrastructure import ControllerResponse, message_response


def update_office_controller(event):
    office_service = office_service_factory()
    user_id = event.pop('user_id')
    office = Office(**event)
    office_updater = OfficeUpdater(office_service)

    try:
        result = office_updater.execute(
            office_id=event['office_id'], office=office, user_id=user_id)

        return ControllerResponse(
            status_code=HTTPStatus.OK if result else HTTPStatus.NOT_FOUND,
            body=result.__dict__ if result else None
        ).__dict__

    except PermissionsError as error:
        return ControllerResponse(
            status_code=HTTPStatus.FORBIDDEN,
            body= message_response(error.args)
        ).__dict__
