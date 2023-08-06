from functools import wraps
from json import dumps
import logging

import flask
from flask import make_response, request

from prison import errors as e

logger = logging.getLogger(__name__)


class ApiDecorator(object):
    def __init__(self):
        self._previous_request_failed = False

    def __call__(self, fn):
        @wraps(fn)
        def newfn(*args, **kwargs):
            try:
                if request.content_length:
                    if (request.mimetype != "application/json"):
                        raise e.ApiException(e.CONTENT_TYPE_JSON_REQUIRED)

                    if "user_id" not in request.json or \
                                    "auth_key" not in request.json:
                        raise e.ApiException(e.CREDENTIALS_REQUIRED)

                result = fn(*args, **kwargs)
            except (e.ApiException) as exc:
                result = exc.flask_error

            if isinstance(result, flask.Flask.response_class):
                return result
            else:
                response = make_response(result)
                if response.data:
                    response.headers["Content-Type"] = "application/json"
                return response

        return newfn


def ok(*args, **kwargs):
    """Simple helper for answering in JSON."""
    if args:
        return dumps(args[0])
    elif kwargs:
        return dumps(kwargs)
    else:
        # OK, but empty response.
        return "", 204
