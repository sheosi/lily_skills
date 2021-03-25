import json
from typing import Dict, Tuple

import requests
from lily_ext import action, add_entity_value, answer, conf, translate

@action(name = "default_action")
class HomeAssistant:

    def __init__(self):
        for name in HomeAssistant.__list_entities().values():
            add_entity_value("device_friendly_name", name, None)

    def trigger_action(self, context):
        entities = HomeAssistant.__list_entities()
        names = {value:key for key, value in entities.items()}
        print(names)

        entity = names[context["device_friendly_name"]]

        HomeAssistant.__call_service("homeassistant",context["intent"], entity_id=entity)
        return answer("Operación completada", context)

    @staticmethod
    def __handle_code(code: int):
        if code == 200 or code == 201:
            return
        elif code == 400:
            raise BadRequestError()
        elif code == 401:
            raise UnauthorizedError()
        elif code == 404:
            raise NotFoundError()
        elif code == 405:
            raise MethodNotAllowedError()

    @staticmethod
    def __make_headers(token: str):
        return {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }

    @staticmethod
    def __post(endpoint, **options):
        ip = conf("ip") #"192.168.1.159"
        port = conf("port") or "8123"
        token = conf("token") # "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI0YWM1NjVhOGJjMTA0ZDcyOWNhZDI5MjY1NmY0ZTA0MCIsImlhdCI6MTYxNjYyNzYxNSwiZXhwIjoxOTMxOTg3NjE1fQ.nlhp5T2sQ_Js1CwAgA2SKOtU-_PDyqqLa1PySi3LOVw"

        r = requests.post(
            f'http://{ip}:{port}/api/{endpoint}',
            headers=HomeAssistant.__make_headers(token),
            data=json.dumps(options))

        HomeAssistant.__handle_code(r.status_code)

    @staticmethod
    def __call_service(domain: str, service: str, **options):
        HomeAssistant.__post(f'services/{domain}/{service}', **options)

    @staticmethod
    def __get(endpoint, **options):
        ip = conf("ip") #"192.168.1.159"
        port = conf("port") or "8123"
        token = conf("token") # "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI0YWM1NjVhOGJjMTA0ZDcyOWNhZDI5MjY1NmY0ZTA0MCIsImlhdCI6MTYxNjYyNzYxNSwiZXhwIjoxOTMxOTg3NjE1fQ.nlhp5T2sQ_Js1CwAgA2SKOtU-_PDyqqLa1PySi3LOVw"

        r = requests.get(
            f'http://{ip}:{port}/api/{endpoint}',
            headers=HomeAssistant.__make_headers(token),
            data=json.dumps(options))
        HomeAssistant.__handle_code(r.status_code)

        return r.json()

    @staticmethod
    def __list_entities() -> Dict[str,str]:
        def get_id(entity) -> Tuple[str, str]:
            name = entity["attributes"].get("friendly_name") or entity["entity_id"]
            return (entity["entity_id"], name)
        return dict(map(get_id, HomeAssistant.__get('states')))

class BadRequestError(ConnectionError):
    """A bad request error ocurred"""

class UnauthorizedError(ConnectionError):
    """An unauthorized error ocurred"""

class NotFoundError(ConnectionError):
    """A not found error ocurred"""

class MethodNotAllowedError(ConnectionError):
    """A method not allowed error ocurred"""

if __name__ == '__main__':
    print("Testing")