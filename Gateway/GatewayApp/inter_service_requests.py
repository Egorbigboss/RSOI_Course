import requests
import json
from typing import Tuple, Dict, List, Union, Any

class ClothGetError(Exception):
     def __init__(self, code: int, err_json: Dict):
         super().__init__()
         self.code = code
         self.err_msg = err_json

class Requester:
    ORDERS_HOST = 'http://127.0.0.1:8001/api/orders/'
    CLOTHS_HOST = 'http://127.0.0.1:8002/api/cloths/'
    ERROR_RETURN = (json.dumps({'error': 'BaseHTTPError was raised!'}), 500)

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
    def get_cloths():
        response = Requester.send_get_request(Requester.CLOTHS_HOST + f'all/')
        print("Response JSON",response.json())
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        return response.json(), response.status_code

    @staticmethod
    def get_concrete_cloth(uuid: str):
        response = Requester.send_get_request(Requester.CLOTHS_HOST + f'{uuid}/')
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        return response.json(), response.status_code

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
        print("Create cloth", response.json())
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
    def get_concrete_user_orders(user_id):
        response = Requester.send_get_request(Requester.ORDERS_HOST + f'user/{user_id}/')
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        print("JSON",response.json())
        response_json = response.json()
        for ord in response_json:
            try:
                ans.append(Requester.__get_and_set_order_attachments(ord))
            except KeyError:
                return (Requester.__create_error_order('Key error was raised, no cloth or audio uuid in order json!'),
                        500)
            except (ClothGetError) as e:
                return e.err_msg, e.code
        return ans, 200

    @staticmethod
    def get_orders():
        response = Requester.send_get_request(Requester.ORDERS_HOST + f'all/')
        if response is None:
            return Requester.ERROR_RETURN
        if response.status_code != 200:
            return response.json(), response.status_code
        print("JSON",response.json())
        response_json = response.json()
        ans = []
        for ord in response_json:
            try:
                ans.append(Requester.__get_and_set_order_attachments(ord))
            except KeyError:
                return (Requester.__create_error_order('Key error was raised, no cloth or audio uuid in order json!'),
                        500)
            except (ClothGetError) as e:
                return e.err_msg, e.code
        return ans, 200



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
            return (Requester.__create_error_order('Key error was raised, no cloth or audio uuid in order json!'),
                    500)
        except (ClothGetError, AudioGetError) as e:
            return e.err_msg, e.code
        return ans, 200
