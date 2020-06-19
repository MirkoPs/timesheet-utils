from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Conflict, BadRequest


def handle_invalid_data(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            raise Conflict("Integrity error: {}".format(e.__cause__))
        except ValueError as e:
            raise BadRequest("Validation error: {}".format(str(e)))

    return wrapper
