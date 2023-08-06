import inspect
import logging

from flask import request
from flask.views import View as _View

logger = logging.getLogger(__name__)


def init_view(view_cls, app, decorator):
    view = decorator(view_cls.as_view(view_cls.__name__))
    methods = inspect.getmembers(view_cls, predicate=inspect.ismethod)
    for name, method in methods:
        for route_args, route_kwargs in getattr(method, "routes", []):
            route_kwargs["endpoint"] = name
            route_kwargs["view_func"] = view
            app.add_url_rule(*route_args, **route_kwargs)


def route(*args, **kwargs):
    def _route(fn):
        try:
            fn.routes.append((args, kwargs))
        except AttributeError:
            fn.routes = [(args, kwargs)]
        return fn

    return _route


class View(_View):
    def dispatch_request(self, *args, **kwargs):
        callback = getattr(self, request.url_rule.endpoint, None)
        assert callback is not None, \
            "Can't dispatch {}: no method {} in {}".format(
                request.url_rule,
                request.url_rule.endpoint,
                self.__class__.__name__)
        return callback(*args, **kwargs)

    @property
    def data(self):
        return request.get_json()

    @property
    def auth_data(self):
        data = self.data
        return data["user_id"], data["auth_key"]

    @property
    def args(self):
        return request.args
