import requests
import json
import re
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
    ERROR_RETURN = (json.dumps({'error': 'BaseHTTPError was raised!'}), 500)
    DELIVERY_HOST = 'http://127.0.0.1:8003/api/delivery/'
    DELIVERY_URL = 'http://127.0.0.1:8000/api/delivery/'



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
    def __create_error_order(msg: str):
        return json.dumps({'error': msg})


    @staticmethod
    def send_post_request(url: str, data: dict):
        try:
            response = requests.post(url=url, data=data)
        except requests.exceptions.BaseHTTPError:
            return None
        return response

    @staticmethod
    def send_get_request(url: str):
        try:
            response = requests.get(url)
        except requests.exceptions.BaseHTTPError:
            return None
        return response

    @staticmethod
    def send_patch_request(url: str, data: dict):
        try:
            response = requests.patch(url=url, json=data)
        except (requests.exceptions.BaseHTTPError):
            return None
        return response

    @staticmethod
    def get_cloths(request):
        url = Requester.CLOTHS_HOST + f'all/'
        cur_url = Requester.CLOTHS_URL
        l_o = Requester.get_limit_offset_from_request(request)
        if l_o is not None:
            url += f'?&limit={l_o[0]}&offset={l_o[1]}'
        response = Requester.send_get_request(url)
        if response is None:
            return Requester.ERROR_RETURN
        response_json = Requester.next_and_prev_links_to_params(response.json(),cur_url)
        return response_json, response.status_code

    @staticmethod
    def get_concrete_cloth(uuid: str):
        response = Requester.send_get_request(Requester.CLOTHS_HOST + f'{uuid}/')
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        return response.json(), response.status_code


    @staticmethod
    def patch_concrete_cloth(uuid: str, data : dict):
        response = Requester.send_patch_request(url = Requester.CLOTHS_HOST + f'{uuid}/', data = data)
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        return response.json(), response.status_code

    @staticmethod
    def patch_concrete_order(uuid: str, data :dict):
        response_order = Requester.send_patch_request(url = Requester.ORDERS_HOST + f'{uuid}/', data = data)
        if response_order is None:
            return Requester.ERROR_RETURN
        if response_order.status_code != 200:
            return response.json(), response.status_code
        cloth_uuid = response_order.json()['cloth_uuid']
        response_cloth = Requester.send_patch_request(url = Requester.CLOTHS_HOST + f'{cloth_uuid}/', data = {
                'type_of_cloth' : response_order.json()['type_of_cloth']
            })
        try:
            ord = Requester.__get_and_set_order_attachments(response_order.json())
        except KeyError:
            return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'),
                    500)
        except (ClothGetError) as e:
            return e.err_msg, e.code
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
    def debug_add_any_cloth(order: Dict):
        cloth_json, cloth_status = Requester.get_cloths()
        if cloth_status == 200:
            order['cloth_uuid'] = cloth_json[0]['uuid']
        return order

    @staticmethod
    def __get_and_set_order_attachments(order: Dict):
        order = Requester.__get_and_set_order_cloth(order)
        return order

    @staticmethod
    def create_cloth(type_of_cloth: str, days_for_clearing: int):
        response = Requester.send_post_request(url=Requester.CLOTHS_HOST + 'all/', data={
            'type_of_cloth' : type_of_cloth,
            'days_for_clearing' : days_for_clearing
        })
        return response.json(), response.status_code

    @staticmethod
    def create_order(type_of_cloth: str, belongs_to_user_id: str, text: str, days_for_clearing: int):
        response_json, code = Requester.create_cloth(type_of_cloth=type_of_cloth, days_for_clearing=days_for_clearing)
        if code == 201:
            cloth_uuid = response_json['uuid']
            response = Requester.send_post_request(url=Requester.ORDERS_HOST + f'user/{belongs_to_user_id}/', data={
                'text' : text,
                'belongs_to_user_id' : belongs_to_user_id,
                'type_of_cloth' : type_of_cloth,
                'cloth_uuid' : cloth_uuid
            })
            return response.json(), response.status_code
        else:
            return response_json, code

    @staticmethod
    def get_concrete_user_orders(request,user_id):
        url = Requester.ORDERS_HOST + f'user/{user_id}/'
        cur_url = Requester.ORDERS_URL + f'user/{user_id}/'
        response = Requester.send_get_request(url)
        l_o = Requester.get_limit_offset_from_request(request)
        if l_o is not None:
            url += f'?&limit={l_o[0]}&offset={l_o[1]}'
        # response = Requester.send_get_request(url)
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        response_json = Requester.next_and_prev_links_to_params(response.json(),cur_url)
        if isinstance(response_json,dict):
            for ord in response_json['results']:
                try:
                    ord = Requester.__get_and_set_order_attachments(ord)
                except KeyError:
                    return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'),
                            500)
                except (ClothGetError) as e:
                    return e.err_msg, e.code
        else:
            for ord in response_json:
                try:
                    ord = Requester.__get_and_set_order_attachments(ord)
                except KeyError:
                    return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'),
                            500)
                except (ClothGetError) as e:
                    return e.err_msg, e.code
        return response_json, 200

    @staticmethod
    def get_orders(request):
        url = Requester.ORDERS_HOST + f'all/'
        l_o = Requester.get_limit_offset_from_request(request)
        if l_o is not None:
            url += f'?&limit={l_o[0]}&offset={l_o[1]}'
        response = Requester.send_get_request(url)
        if response is None:
            return Requester.ERROR_RETURN
        response_json = Requester.next_and_prev_links_to_params(response.json(),Requester.ORDERS_URL)
        if isinstance(response_json,dict):
            for ord in response_json['results']:
                try:
                    ord = Requester.__get_and_set_order_attachments(ord)
                except KeyError:
                    return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'),
                            500)
                except (ClothGetError) as e:
                    return e.err_msg, e.code
        else:
            for ord in response_json:
                try:
                    ord = Requester.__get_and_set_order_attachments(ord)
                except KeyError:
                    return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'),
                            500)
                except (ClothGetError) as e:
                    return e.err_msg, e.code
        return response_json, 200

    def get_concrete_user_delivery(request,user_id):
        url = Requester.DELIVERY_HOST + f'user/{user_id}/'
        cur_url = Requester.DELIVERY_URL + f'user/{user_id}/'
        response = Requester.send_get_request(url)
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
    def create_delivery_list(request,user_id):
        url=Requester.DELIVERY_HOST + f'user/{user_id}/'
        response,code = Requester.get_concrete_user_orders(request,user_id=user_id)
        if code != 200:
            return response, response.status_code
        ans = []
        for ord in response:
                cur_json = Requester.send_post_request(url=url, data = {
                    'user_id' : user_id,
                    'order_uuid' : ord['uuid'],
                    'date_of_creation' : ord['date_of_creation'],
                    'days_for_clearing': ord['cloth']['days_for_clearing']
                })
                ans.append(cur_json.json())
        return ans, status.HTTP_200_OK



    @staticmethod
    def get_concrete_order(uuid: str):
        response = Requester.send_get_request(Requester.ORDERS_HOST + f'{uuid}/')
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        response_json = response.json()
        try:
            ans = Requester.__get_and_set_order_attachments(response_json)
        except KeyError:
            return (Requester.__create_error_order('Key error was raised, no cloth uuid in order json!'),
                    500)
        except (ClothGetError) as e:
            return e.err_msg, e.code
        return ans, 200
