from datetime import datetime, time
from typing import List

from desk_reservation.ride.domain import RideBooking, Ride
from desk_reservation.ride.domain.services.ride_service import RideService
from desk_reservation.users.domain.services import UserService
from desk_reservation.shared.domain import SlackMessageService
from desk_reservation.shared.infrastructure import Criteria, Operator, Filter
from ..message_templates.ride_templates import DRIVER_REMINDER_TEMPLATE, RIDER_REMINDER_TEMPLATE


class DriverAndRiderReminder:
    def __init__(
            self,
            slack_message_service: SlackMessageService,
            ride_service: RideService,
            user_service: UserService):
        self.slack_message_service = slack_message_service
        self.ride_service = ride_service
        self.user_service = user_service

    async def execute(self):
        template_driver = self.slack_message_service.choise_template(
            DRIVER_REMINDER_TEMPLATE)
        template_rider = self.slack_message_service.choise_template(
            RIDER_REMINDER_TEMPLATE)
        today = datetime.today()
        start_of_day = datetime.combine(today, time.min)
        end_of_day = datetime.combine(today, time.max)
        criteria_ride = Criteria(
            filters=[
                Filter(
                    field="ride_date",
                    operator=Operator.GREATER_EQUAL_THAN,
                    value=start_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                ),
                Filter(
                    field="ride_date",
                    operator=Operator.LOWER_EQUAL_THAN,
                    value=end_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                ),
                Filter(field="deleted_at", operator=Operator.EQUAL, value=None),
            ]
        )
        rides = self.ride_service.find_all(criteria=criteria_ride)
        for ride in rides:
            await self.send_message(ride, template_driver, template_rider)

    async def get_passengers_ids(self, passengers: List[RideBooking]) -> str:
        passengers_ids = []
        for passenger in passengers:
            slack_id = await self.get_slack_id(passenger.user_id)
            passengers_ids.append(slack_id)
        return passengers_ids

    async def get_slack_id(self, user_id: str) -> str:
        user = self.user_service.get_user(user_id)
        return await self.slack_message_service.get_user_id_by_email(
            user.email)

    async def send_message(self, ride: Ride, template_driver: str, template_rider: str):
        criteria_booking_ride = Criteria(
            filters=[
                Filter(
                    field="ride_id",
                    operator=Operator.EQUAL,
                    value=ride.ride_id,
                ),
                Filter(field="deleted_at",
                       operator=Operator.EQUAL, value=None),
            ]
        )
        slack_id = await self.get_slack_id(ride.offerer_user_id)
        passengers = self.ride_service.find_booking_ride(
            criteria=criteria_booking_ride)

        print('passengers', passengers)
        if len(passengers) == 0:
            return

        passengers_ids = await self.get_passengers_ids(passengers)
        for passenger_id in passengers_ids:
            message = template_rider.format(
                username=f'<@{passenger_id}>',
                date=ride.ride_date.strftime("%Y-%m-%d"),
                driver_user_name=f'<@{slack_id}>',
            )
            await self.slack_message_service.send_message_by_user_email(
                message=message, user_id=passenger_id)

        passengers_ids_str = ', '.join(
            [f'<@{id}>' for id in passengers_ids])
        format_template = template_driver.format(
            username=f'<@{slack_id}>',
            date=ride.ride_date.strftime("%Y-%m-%d"),
            riders_username=passengers_ids_str)

        await self.slack_message_service.send_message_by_user_email(
            user_id=slack_id,
            message=format_template,
        )
