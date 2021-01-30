from sqlalchemy.exc import IntegrityError, InternalError
from werkzeug.exceptions import Conflict, BadRequest


def handle_invalid_data(func):
    def wrapper(*args, **kwargs):
        try:
            if 'data' in kwargs.keys() and not kwargs['data']:
                raise BadRequest("Body request not valid!")
            return func(*args, **kwargs)
        except IntegrityError as e:
            raise Conflict("Integrity error: {}".format(e.__cause__))
        except InternalError as e:
            raise BadRequest("Internal error: {}".format(e.__cause__))
        except ValueError as e:
            raise BadRequest("Validation error: {}".format(str(e)))

    return wrapper
