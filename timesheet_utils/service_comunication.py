import requests as http_requests
from flask import redirect as flask_redirect
from flask import request as flask_request
from flask_restplus import abort
from py_eureka_client import eureka_client
from werkzeug.exceptions import Unauthorized


def get_authorization_header():
    auth = flask_request.headers.get('Authorization')
    if not auth:
        raise Unauthorized('Missing authorization!')

    return {'Authorization': flask_request.headers.get('Authorization')}


def request(app_name, api_request, method='GET', check_ok=True):
    def method_error():
        raise ValueError('Method {} is not available!'.format(method))

    def do_request(url):
        headers = {'Authorization': flask_request.headers.get('Authorization')}
        request_func = getattr(http_requests, method.lower(), method_error)
        return request_func(url, headers=headers)

    response = eureka_client.walk_nodes(app_name, api_request, prefer_ip=True, prefer_https=False, walker=do_request)

    if check_ok and response.status_code != 200:
        abort(response.status_code, response.json()['message'])

    return response
