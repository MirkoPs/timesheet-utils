from timesheet_utils.service_comunication import request
from werkzeug.exceptions import Unauthorized, Forbidden
import os

def get_logged_user():
    users_base_url_port = os.environ.get('USERS_SERVICE_BASE_URL_PORT')
    data = request('{}/users/me/'.format(users_base_url_port), check_ok=False)
    if data.status_code != 200:
        print("'/users/me/' returned '{}' status".format(data.status_code))
        raise Unauthorized(data.json()['msg'])

    return eval(data.content)


def require_login(only_with_roles: list = None):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            user = get_logged_user()
            kwargs['user'] = user

            user_role = user['role']['name']
            if only_with_roles and user_role not in only_with_roles:
                raise Forbidden("'{}' role  is not allowed to get this content!".format(user_role))

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
