import logging

from prison.apiutils import ok
from prison.client.card import is_can_play, play, finish
from prison.views import View, route
from prison import  errors as e
logger = logging.getLogger(__name__)


class CardView(View):
    @route("/v1/card", methods=["GET"])
    def _is_can_play(self):
        user_id, auth_key = self.auth_data
        return ok({
            "available": is_can_play(user_id, auth_key)
        })

    @route("/v1/card", methods=["POST"])
    def _play_full_game(self):
        user_id, auth_key = self.auth_data

        if not is_can_play(user_id, auth_key):
            raise e.ApiException(e.CARD_GAME_NOT_AVAILABLE)

        result = play(user_id, auth_key)
        if result is None:
            raise e.ApiException(e.CARD_GAME_PLAY_ERROR)

        result = finish(user_id, auth_key)
        if result is None:
            raise e.ApiException(e.CARD_GAME_PLAY_ERROR)

        return ok(rewards=result)
