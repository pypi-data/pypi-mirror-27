""" iven cloud api """
from hashlib import sha1
import hmac
import requests
import json
from models import IvenResponse, Error, Task

base_url = "staging.iven.io"
activation_url = "http://"+base_url+"/activate/device"
data_url = "http://"+base_url+"/data"
api_key = None


def set_cloud_address(address):
    if address is not None and isinstance(address, str):
        global base_url, activation_url, data_url
        base_url = address
        activation_url = "http://"+base_url+"/activate/device"
        data_url = "http://"+base_url+"/data"


def activate_device(secret_key, device_uid):
    """
    Activates device in Iven Cloud.
    Devices must be activate first to be able to send data.

    :param secret_key: string
    :param device_uid: string
    :return: IvenResponse object on success, None on error
    """
    response = IvenResponse()
    if device_uid is not None and isinstance(device_uid, str) and \
                    secret_key is not None and isinstance(secret_key, str) and \
            bool(device_uid) and bool(secret_key):
        global api_key

        # HMAC-SHA1 encryption to get activation code
        hashed = hmac.new(secret_key, device_uid, sha1)
        activation_code = hashed.digest().encode("hex")
        headers = {'Activation': activation_code, 'Content-Type': "application/json"}

        r = requests.get(activation_url, headers=headers)
        response.status = r.status_code
        if r.status_code < 500 and 'application/json' in r.headers['Content-Type']:
            response_body = r.json()
            if 'api_key' in response_body:
                api_key = response_body['api_key']
                response.api_key = api_key
            if 'description' in response_body:
                response.description = response_body['description'].encode('utf-8')
            if 'ivenCode' in response_body:
                response.iven_code = response_body['ivenCode']
    else:
        response.error = Error(0, "Secret key or device_uid is not valid")

    return response


def send_data(datas):
    """
    Sends data to Iven Cloud
    Device must be activated to be able to send data

    :param datas: dictionary
    :return: IvenResponse object on success, error codes on error
    """

    payload = {"data": []}
    payload['data'].append(datas)

    return send_data_request(payload)


def task_done(task_iven_code):
    payload = {
        "iven_code": str(task_iven_code),
        "data": [{"FEED": "TD"}]
    }

    return send_data_request(payload)


def send_data_request(payload):
    response = IvenResponse()
    if api_key is not None:
        if isinstance(payload, dict):
            headers = {'API-KEY': api_key, 'Content-Type': "application/json"}
            r = requests.post(data_url, data=json.dumps(payload), headers=headers)
            response.status = r.status_code
            if r.status_code < 500 and 'application/json' in r.headers['Content-Type']:
                response_body = r.json()
                if 'description' in response_body:
                    response.description = response_body['description'].encode('utf-8')
                elif 'message' in response_body:
                    response.description = response_body['message'].encode('utf-8')
                    if 'UPDATE_REQUIRED' in response_body['message']:
                        response.need_firm_update = True
                    if 'CONFIGURATION_UPDATE_REQUIRED' in response_body['message']:
                        response.need_conf_update = True

                if 'ivenCode' in response_body:
                    response.iven_code = response_body['ivenCode']

                    if response.iven_code > 1000:
                        task = None
                        if 'task' in response_body:
                            task = response_body['task'].encode('utf-8')
                        response.task = Task(response_body['ivenCode'], task)
        else:
            # datas is NULL or not valid format
            response.error = Error(0, "Data is not valid format")
    else:
        # Api key is not set
        response.error = Error(0, "API-KEY is not set")

    return response

