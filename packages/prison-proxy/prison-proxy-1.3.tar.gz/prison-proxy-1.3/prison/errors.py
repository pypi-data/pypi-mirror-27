import json


def get_error_code(error):
    if isinstance(error, tuple):
        return error[0]
    else:
        return error


def make_flask_error(error, **kwargs):
    error_code, http_code = error if isinstance(error, tuple) else (error, 400)
    d = {"error": error_code}
    d.update(kwargs)
    return json.dumps(d), http_code


class ApiException(Exception):
    """
    Exception used to indicate some API error.
    """

    def __init__(self, error, **kwargs):
        self.error = error
        self.error_kwargs = kwargs

    @property
    def error_code(self):
        return get_error_code(self.error)

    @property
    def flask_error(self):
        return make_flask_error(self.error, **self.error_kwargs)


CONTENT_TYPE_JSON_REQUIRED = "content_type_json_required"
CREDENTIALS_REQUIRED = "credentials_required"

# Cards
CARD_GAME_NOT_AVAILABLE = "card_game_not_available"
CARD_GAME_PLAY_ERROR = "card_game_error_raised_while_play"
CARD_GAME_FINISH_ERROR = "card_game_error_raised_while_finish"

# Slot
SLOT_BET_ERROR = "slot_bet_error"
SLOT_PLAY_ERROR = "slot_error_raised_while_play"