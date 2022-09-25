from http import HTTPStatus

from ...application import OfficeFinderOne
from ....shared.infrastructure import ControllerResponse
from ....shared.infrastructure.dependency_injection.services_factory import office_service_factory


def get_office_controller(event):
    office_service = office_service_factory()
    office_finder_one = OfficeFinderOne(office_service)

    result = office_finder_one.execute(event['office_id'])
    response = (HTTPStatus.OK, result.__dict__) if result else (
        HTTPStatus.NOT_FOUND, None)
    return ControllerResponse(
        status_code=response[0],
        body=response[1]
    ).__dict__
