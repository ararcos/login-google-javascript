import asyncio
from typing import Optional
from functools import partial
import requests


class RestClient:

    def __init__(
            self,
            base_url: str,
            api_token: str,
    ) -> 'RestClient':

        self.base_url = base_url.rstrip('/')
        self.headers = {'Authorization': f'Bearer {api_token}'}

    async def get(
        self,
        additional_url: str = '',
        query_params: Optional[dict] = None,
        custom_headers: Optional[dict] = None
    ) -> requests.Response:

        headers_to_send = {**self.headers, **
                           custom_headers} if custom_headers else self.headers
        partial_get = partial(requests.get, f'{self.base_url}/{additional_url}',
                              params=query_params or {}, headers=headers_to_send)
        return await asyncio.get_event_loop().run_in_executor(None, partial_get)

    async def post(
        self, additional_url: str = '',
        payload: Optional[dict] = None,
        query_params: Optional[dict] = None,
        custom_headers: Optional[dict] = None
    ) -> requests.Response:

        headers_to_send = {**self.headers, **
                           custom_headers} if custom_headers else self.headers
        partial_post = partial(requests.post, f'{self.base_url}/{additional_url}',
                               params=query_params or {}, json=payload, headers=headers_to_send)
        return await asyncio.get_event_loop().run_in_executor(None, partial_post)
