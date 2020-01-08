from GatewayApp.requests_lib import Requests

from typing import Tuple, Dict
import requests
from requests.exceptions import RequestException

class Job(Requests):

    def post(url: str, data: dict):
        # response = super().post(url = self.URL, data = data, headers = headers)
        response = requests.post(url, data)
        return response

    # def delete(self, payload: dict) -> int:
    #     uuid, headers = payload['uuid'], payload['headers']

    #     response = super().delete(url = f'{self.URL}{uuid}/', headers = headers)
    #     return response.status_code

    @staticmethod
    def patch(url: str, data: dict):
        response = requests.patch(url, data)
        return response