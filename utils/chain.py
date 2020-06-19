from abc import ABC, abstractmethod
from typing import Any


class Handler(ABC):

    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, *args, **kwargs):
        pass


class AbstractHandler(Handler):
    _next_handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, *args, **kwargs) -> Any:
        if self._next_handler:
            return self._next_handler.handle(*args, **kwargs)

        return None


class RoleHandler(AbstractHandler):

    def __init__(self, roles: list, func):
        self.roles: list = roles
        self.func = func

    def handle(self, *args, **kwargs):
        user = kwargs.get('user')
        if user['role']['name'] in self.roles:
            return self.func(*args, **kwargs)

        return super().handle(*args, **kwargs)


class EndHandler(AbstractHandler):

    def handle(self, *args, **kwargs) -> Any:
        raise ValueError("Request doesn't match any handler in chain.")


def get_chain(handlers: list) -> AbstractHandler:
    if not handlers:
        raise ValueError("No handlers to chain.")

    chain = EndHandler()

    for handler in handlers[::-1]:
        handler.set_next(chain)
        chain = handler

    return chain
