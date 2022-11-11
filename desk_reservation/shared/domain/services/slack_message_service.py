from typing import List
from random import choice
from ...infrastructure import SlackRepository, Channel


class SlackMessageService:
    def __init__(
        self,
        slack_repository: SlackRepository,
    ):
        self.slack_repository = slack_repository

    async def get_user_id_by_email(self, email: str):
        return await self.slack_repository.get_user_id_by_email(email=email)

    async def send_message_by_user_email(self, message: str, user_id: str):
        await self.slack_repository.send_message(text_message=message, receiver=user_id)

    async def send_message_by_users_email(self, emails: List[str], message: str):
        users_id = await self.slack_repository.get_users_id_by_email(users_email=emails)
        await self.slack_repository.send_many_messages(text_message=message, receivers=users_id)

    async def send_message_by_office(self, office: str, message: str):
        channel_id = self.get_channel_id_by_office(office=office)
        await self.slack_repository.send_message(text_message=message, receiver=channel_id)

    async def send_message_by_offices(self, offices: List[str], message: str):
        channels_id = map(self.get_channel_id_by_office, offices)
        await self.slack_repository.send_many_messages(text_message=message, receivers=channels_id)

    def get_channel_id_by_office(self, office: str) -> str:
        channels = {
            'quito': Channel.QUITO,
            'guayaquil': Channel.GUAYAQUIL,
            'loja': Channel.LOJA,
        }
        return channels.get(office) or Channel.TEST

    def choise_template(self, template: List[str]) -> str:
        return choice(template)
