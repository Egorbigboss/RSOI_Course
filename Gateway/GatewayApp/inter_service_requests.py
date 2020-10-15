import requests
import json
import re
import pybreaker
import redis
from GatewayApp.my_queue import ReqQueue
from GatewayApp.requests_lib import Requests

from typing import Tuple, Dict, List, Union, Any
from rest_framework import status

class ClothGetError(Exception):
     def __init__(self, code: int, err_json: Dict):
         super().__init__()
         self.code = code
         self.err_msg = err_json

class Requester:

    ORDERS_URL = 'http://127.0.0.1:8000/api/orders/'
    CLOTHS_URL = 'http://127.0.0.1:8000/api/cloths/'
    ORDERS_HOST = 'http://127.0.0.1:8001/api/orders/'
    CLOTHS_HOST = 'http://127.0.0.1:8002/api/cloths/'
    DELIVERY_HOST = 'http://127.0.0.1:8003/api/delivery/'
    DELIVERY_URL = 'http://127.0.0.1:8000/api/delivery/'
    AUTH_HOST = 'http://127.0.0.1:8004/api/'
    AUTH_URL = 'http://127.0.0.1:8000/user/'
    STATS_HOST = 'http://127.0.0.1:8005/api/stats/'
    STATS_URL = 'http://127.0.0.1:8000/api/stats/'
    ERROR_RETURN = (json.dumps({'error': 'BaseHTTPError was raised!'}), 500)
    ERROR_CREATE = (json.dumps({'error': 'Connection refused by one of the services!'}), 500)

    @staticmethod
    def pybreaker_error():
         return json.dumps({'error': f'Circut breaker is now working'}), 500

    @staticmethod
    def __create_error_order(msg: str):
        return json.dumps({'error': msg})


    def get_limit_offset_from_request(request):
        try:
            limit = request.query_params['limit']
            offset = request.query_params['offset']
        except KeyError:
            return None
        return limit, offset

    def find_limit_and_offset_in_link(link: str):
        limit_substr = re.findall(r'limit=\d+', link)
        offset_substr = re.findall(r'offset=\d+', link)
        limit = re.findall(r'\d+', limit_substr[0])
        offset = [0]
        if len(offset_substr) != 0:
            offset = re.findall(r'\d+', offset_substr[0])
        return limit[0], offset[0]

    def next_and_prev_links_to_params(data: dict,current_host: str):
        try:
            next_link, prev_link = data['next'], data['previous']
        except (KeyError, TypeError):
             return data
        if next_link:
            limit, offset = Requester.find_limit_and_offset_in_link(next_link)
            data['next'] = current_host + f'?limit={limit}&offset={offset}'
        if prev_link:
            limit, offset = Requester.find_limit_and_offset_in_link(prev_link)
            data['previous'] = current_host + f'?limit={limit}&offset={offset}'
        return data

    @staticmethod
    def delete_cloth(request , cloth_uuid: str):
        try:
            response = Requests.send_delete_request(Requester.CLOTHS_HOST + f'{cloth_uuid}')
        except requests.exceptions.BaseHTTPError:
            return None
        return response.status_code

    @staticmethod
    def get_cloths(request):
        url = Requester.CLOTHS_HOST + f'all/'
        cur_url = Requester.CLOTHS_URL
        l_o = Requester.get_limit_offset_from_request(request)
        if l_o is not None:
            url += f'?&limit={l_o[0]}&offset={l_o[1]}'
        try:
            response = Requests.send_get_request(url)
        except pybreaker.CircuitBreakerError:
            return Requester.pybreaker_error()
        except ValueError:
            return Requester.ERROR_RETURN
        response_json = Requester.next_and_prev_links_to_params(response.json(),cur_url)
        return response_json, response.status_code

    @staticmethod
    def get_concrete_cloth(uuid: str):
        try:
            response = Requests.send_get_request(Requester.CLOTHS_HOST + f'{uuid}/')
        except pybreaker.CircuitBreakerError:
            return Requester.pybreaker_error()
        except ValueError:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        return response.json(), response.status_code


    @staticmethod
    def patch_concrete_cloth(uuid: str, data : dict):
        try:
            response = Requests.send_patch_request(url = Requester.CLOTHS_HOST + f'{uuid}/', data = data)
        except pybreaker.CircuitBreakerError:
            return Requester.pybreaker_error()
        except ValueError:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        return response.json(), response.status_code

    @staticmethod
    def patch_concrete_order(uuid: str, data :dict):
        try:
            response_order = Requests.send_patch_request(url = Requester.ORDERS_HOST + f'{uuid}/', data = data)
            if response_order.status_code != 200:
                return response_order.json(), response_order.status_code
        except ValueError:
            return Requester.ERROR_RETURN
        cloth_uuid = response_order.json()['cloth_uuid']
        print("tut?")
        try:
            response_cloth = Requests.send_patch_request(url = Requester.CLOTHS_HOST + f'{cloth_uuid}/', data = {
                    'type_of_cloth' : response_order.json()['type_of_cloth']
                })
        except ValueError:
            ReqQueue.add_patch_task_to_queue(url = Requester.CLOTHS_HOST + f'{cloth_uuid}/', data = {
                    'type_of_cloth' : response_order.json()['type_of_cloth']
                })
            return Requester.ERROR_RETURN[0], 200
        try:
            ord = Requester.__get_and_set_order_cloth(response_order.json())
        except KeyError:
            return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'), 500)
        except (ClothGetError) as e:
            return e.err_msg, e.code
        ReqQueue.unqueue_tasks_from_queue()
        return ord, 200

    @staticmethod
    def __get_and_set_order_cloth(order: Dict):
        cloth_uuid = order['cloth_uuid']
        if cloth_uuid is not None:
            cloth_json, cloth_status = Requester.get_concrete_cloth(cloth_uuid)
            if cloth_status != 200:
                raise ClothGetError(code=cloth_status, err_json=cloth_json)
            order['cloth'] = cloth_json
        else:
            raise KeyError
        return order

    @staticmethod
    def create_cloth(type_of_cloth: str, days_for_clearing: int):
        try:
            response = Requests.send_post_request(url=Requester.CLOTHS_HOST + 'all/', data={
                'type_of_cloth' : type_of_cloth,
                'days_for_clearing' : days_for_clearing
            })
        except pybreaker.CircuitBreakerError:
            return Requester.pybreaker_error()
        return response.json(), response.status_code

    @staticmethod
    def create_order(request, type_of_cloth: str, belongs_to_user_id: str, text: str, days_for_clearing: int):
        response_json, code = Requester.create_cloth(type_of_cloth=type_of_cloth, days_for_clearing=days_for_clearing)
        if code == 201:
            cloth_uuid = response_json['uuid']
            try:
                response = Requests.send_post_request(url=Requester.ORDERS_HOST + f'user/{belongs_to_user_id}/', data={
                    'text' : text,
                    'belongs_to_user_id' : belongs_to_user_id,
                    'type_of_cloth' : type_of_cloth,
                    'cloth_uuid' : cloth_uuid
                })
                if response.status_code != 201:
                    try:
                        response = Requester.delete_cloth(request , cloth_uuid)
                    except KeyError:
                        pass
                    return Requester.ERROR_RETURN
            except ValueError:
                try:
                    response = Requester.delete_cloth(request , cloth_uuid)
                except KeyError:
                    pass
                return Requester.ERROR_RETURN
        else:
            return response_json, code

    @staticmethod
    def get_concrete_user_orders(request, user_id: int):
        url = Requester.ORDERS_HOST + f'user/{user_id}/'
        cur_url = Requester.ORDERS_URL + f'user/{user_id}/'
        try:
            response = Requests.send_get_request(url)
        except ValueError:
            return Requester.ERROR_RETURN
        l_o = Requester.get_limit_offset_from_request(request)
        if l_o is not None:
            url += f'?&limit={l_o[0]}&offset={l_o[1]}'
        if response.status_code != 200:
            return response.json(), response.status_code
        response_json = Requester.next_and_prev_links_to_params(response.json(),cur_url)
        if isinstance(response_json,dict):
            for ord in response_json['results']:
                try:
                    ord = Requester.__get_and_set_order_cloth(ord)
                except ValueError:
                    ord['cloth'] = None
                except ClothGetError:
                    return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'),
                            500)
        else:
            for ord in response_json:
                try:
                    ord = Requester.__get_and_set_order_cloth(ord)
                except ValueError:
                    ord['cloth'] = None
                except ClothGetError:
                    return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'),
                            500)
        return response_json, 200

    @staticmethod
    def get_orders(request):
        url = Requester.ORDERS_HOST + f'all/'
        l_o = Requester.get_limit_offset_from_request(request)
        if l_o is not None:
            url += f'?&limit={l_o[0]}&offset={l_o[1]}'
        try:
            response = Requests.send_get_request(url)
        except ValueError:
            return Requester.ERROR_RETURN
        response_json = Requester.next_and_prev_links_to_params(response.json(),Requester.ORDERS_URL)
        if isinstance(response_json,dict):
            for ord in response_json['results']:
                try:
                    ord = Requester.__get_and_set_order_cloth(ord)
                except ValueError:
                    ord['cloth'] = None
                except ClothGetError:
                    return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'),
                            500)
        else:
            for ord in response_json:
                try:
                    ord = Requester.__get_and_set_order_cloth(ord)
                except ValueError:
                    ord['cloth'] = None
                except ClothGetError:
                    return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'),
                            500)
        return response_json, 200

    def get_concrete_user_delivery(request,user_id: int):
        url = Requester.DELIVERY_HOST + f'user/{user_id}/'
        cur_url = Requester.DELIVERY_URL + f'user/{user_id}/'
        try:
            response = Requests.send_get_request(url)
        except pybreaker.CircuitBreakerError:
            return Requester.pybreaker_error()
        l_o = Requester.get_limit_offset_from_request(request)
        if l_o is not None:
            url += f'?&limit={l_o[0]}&offset={l_o[1]}'
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        response_json = Requester.next_and_prev_links_to_params(response.json(),cur_url)
        return response_json, 200


    @staticmethod
    def create_delivery_list(request, user_id: int ):
        url=Requester.DELIVERY_HOST + f'user/{user_id}/'
        response,code = Requester.get_concrete_user_orders(request,user_id=user_id)
        if code != 200:
            return response, response.status_code
        ans = []
        for ord in response:
            try:
                cur_json = Requests.send_post_request(url=url, data = {
                    'user_id' : user_id,
                    'order_uuid' : ord['uuid'],
                    'date_of_creation' : ord['date_of_creation'],
                    'days_for_clearing': ord['cloth']['days_for_clearing']
                })
                ans.append(cur_json.json())
            except pybreaker.CircuitBreakerError:
                return Requester.pybreaker_error()
        return ans, status.HTTP_200_OK



    @staticmethod
    def get_concrete_order(uuid: str):
        try:
            response = Requests.send_get_request(Requester.ORDERS_HOST + f'{uuid}/')
            response_json = response.json()
            try:
                ans = Requester.__get_and_set_order_cloth(response_json)
            except KeyError:
                return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'), 500)
            except (ClothGetError) as e:
                return e.err_msg, e.code
            return ans, 200
        except ValueError:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code



    @staticmethod
    def retrieve_token_from_request(request):
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        return token


    @staticmethod 
    def authenticate_user(request, data: dict):
        response = Requests.send_post_request(Requester.AUTH_HOST + f'token_auth/', data=data)
        if response is None:
            return Requester.ERROR_RETURN
        return response.json(), response.status_code

    @staticmethod
    def check_token(request):
        token = Requester.retrieve_token_from_request(request)
        response = Requests.send_get_request(Requester.AUTH_HOST + f'check_token/', headers = {'Authorization': f'Token {token}'})
        return response.status_code == 200

    @staticmethod
    def get_user(request):
        token = Requester.retrieve_token_from_request(request)
        response = Requests.send_get_request(Requester.AUTH_HOST + f'check_token/', headers = {'Authorization': f'Token {token}'})
        return response.json(), response.status_code


    @staticmethod
    def collect_stats(request):
        response = Requests.send_get_request(Requester.STATS_HOST + f'all/')
        return response.json(), response.status_code


    @staticmethod
    def create_metric(request, data: dict):
        response = Requests.send_post_request(Requester.STATS_HOST + f'all/', data = data)
        return response.json(), response.status_code



    @staticmethod
    def update_metric(requset, data: dict):
        if data['type_of_object'] == 'orders':
            response = Requests.send_get_request(Requester.ORDERS_HOST + f'stats/')
            # response = requests.get
            if response.status_code == 200:
                days = json.dumps(response.json()['days'])
                print(days)
                response_ord = Requests.send_patch_request(Requester.STATS_HOST + f'update/', data = {'filter' : 'dates', 'days' : days})
                return response_ord.json(), response_ord.status_code
        else:
            response = Requests.send_get_request(Requester.CLOTHS_HOST + f'stats/', data = {'type_of_object' : data['type_of_object']})
            if response.status_code == 200:
                response_cloth = Requests.send_patch_request(Requester.STATS_HOST + f'update/', data = {'filter' : data['type_of_object'], 'count' : response.json()['count']})
                return response_cloth.json(), response_cloth.status_code
        


    @staticmethod
    def get_concrete_metric(request, stat_uuid):
        response = Requester.send_post_request(Requester.STATS_HOST + f'{stat_uuid}')
        return response.json(), response.status_code