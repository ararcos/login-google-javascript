from asyncio import gather
from typing import List
from decouple import config
from .rest_client.rest_client import RestClient


class SlackRepository:
    api_token = config('slack_token')
    limit = 190
    client = RestClient(
        base_url='https://slack.com/api/',
        api_token=api_token,
    )

    @classmethod
    async def get_user_by_email(cls, email):
        query_params = {
            'email': email
        }
        response = await cls.client.get('users.lookupByEmail', query_params=query_params)
        user = response.json()

        cls.raise_exception_for_error(user, cls.get_user_by_email.__name__)
        return user.get('user')

    @classmethod
    async def get_users_id_by_email(cls, users_email: List[str]) -> List[str]:
        users = await gather(*[cls.get_user_by_email(email) for email in users_email])
        return map(lambda user: user.get('id'), users)

    @classmethod
    async def get_user_id_by_email(cls, email: str) -> str:
        user = await cls.get_user_by_email(email)
        return user.get('id')

    @classmethod
    async def send_message(cls, text_message: str, receiver: str):
        response = await cls.client.post('chat.postMessage', payload={
            'text': text_message,
            'channel': receiver
        })
        return response

    @classmethod
    async def send_many_messages(cls, text_message: str, receivers: List[str]):
        await gather(*[cls.send_message(text_message, receiver) for receiver in receivers])

    @staticmethod
    def raise_exception_for_error(response: dict, function_name: str):
        if not response.get('ok'):
            error = response.get('error')
            raise Exception(
                f'Could not retrieve information on {function_name}, due the following error: {error}')
