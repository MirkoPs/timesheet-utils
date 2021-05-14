import requests as http_requests
from flask import redirect as flask_redirect
from flask import request as flask_request
from flask_restplus import abort
# from py_eureka_client import eureka_client
from werkzeug.exceptions import Unauthorized


def get_authorization_header():
    auth = flask_request.headers.get('Authorization')
    if not auth:
        raise Unauthorized('Missing authorization!')

    return {'Authorization': flask_request.headers.get('Authorization')}


def request(api_request_url, method='GET', check_ok=True):
    def method_error(*args, **kwargs):
        raise ValueError('Method {} is not available!'.format(method))

    def do_request(url):
        headers = {'Authorization': flask_request.headers.get('Authorization')}
        request_func = getattr(http_requests, method.lower(), method_error)
        return request_func(url, headers=headers)

    response = do_request(api_request_url)

    if check_ok and response.status_code != 200:
        abort(response.status_code, response.json()['message'])

    return response
