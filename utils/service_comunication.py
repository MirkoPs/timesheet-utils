import requests as http_requests
from flask import redirect as flask_redirect
from flask import request as flask_request
from flask_restplus import abort

services = {
    'USER_SERVICE': '127.0.0.1:5001',
    'EMPLOYEE_SERVICE': '127.0.0.1:5000',
    'EMPLOYEE_COST_SERVICE': '127.0.0.1:5002',
    'TIMESHEET_SERVICE': '127.0.0.1:5003',
    'TIMESHEET_DETAIL_SERVICE': '127.0.0.1:5004',
    'PROJECT_ACTIVITY_SERVICE': '127.0.0.1:5005',
    'PROJECT_SERVICE': '127.0.0.1:5006',
    'CUSTOMER_SERVICE': '127.0.0.1:5007',
}


def request(service_name, api_request, request_type='GET', check_ok=True):
    url = 'http://{}/{}'.format(services[service_name], api_request)
    headers = {'Authorization': flask_request.headers.get('Authorization')}
    if request_type == 'GET':
        response = http_requests.get(url, headers=headers)
    elif request_type == 'DELETE':
        response = http_requests.delete(url, headers=headers)
    else:
        raise ValueError('request_type {} is not valid!'.format(request_type))

    if check_ok and response.status_code != 200:
        abort(response.status_code, response.json()['message'])

    return response


def redirect(service_name, api_request):
    return flask_redirect(
        'http://{}/{}'.format(services[service_name], api_request),
        code=307
    )
