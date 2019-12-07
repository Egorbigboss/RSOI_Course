import pybreaker
import redis
from typing import Tuple, Dict, List, Union, Any
from rest_framework import status
import requests



class Requests:

    redis = redis.StrictRedis(password='test')
    db_breaker = pybreaker.CircuitBreaker(
        fail_max=5,
        reset_timeout=15,
        state_storage=pybreaker.CircuitRedisStorage(pybreaker.STATE_CLOSED, redis)
    )

    @staticmethod
    def get_request(url: str):
        try:
            response = requests.get(url)
        except (requests.exceptions.BaseHTTPError, requests.ConnectionError):
            return None
        return response

    @staticmethod
    def post_request(url: str, data: dict):
        try:
            response = requests.post(url, data)
        except (requests.exceptions.BaseHTTPError, requests.ConnectionError):
            return None
        return response

    @staticmethod
    def patch_request(url: str, data: dict):
        try:
            response = requests.patch(url, data)
        except (requests.exceptions.BaseHTTPError, requests.ConnectionError):
            return None
        return response

    @staticmethod
    def delete_request(url: str):
        try:
            response = requests.delete(url)
        except (requests.exceptions.BaseHTTPError, requests.ConnectionError):
            return None
        return response

    @db_breaker
    def send_post_request(url: str, data: dict):
        response = Requests.post_request(url, data)
        if response is None:
            raise ValueError
        return response

    @db_breaker
    def send_get_request(url: str):
        response = Requests.get_request(url)
        if response is None:
            raise ValueError
        return response

    @db_breaker
    def send_patch_request(url: str, data: dict):
        response = Requests.patch_request(url, data)
        if response is None:
            raise ValueError
        return response

    @db_breaker
    def send_delete_request(url: str):
        response = Requests.delete_request(url)
        if response is None:
            raise ValueError
        return response
