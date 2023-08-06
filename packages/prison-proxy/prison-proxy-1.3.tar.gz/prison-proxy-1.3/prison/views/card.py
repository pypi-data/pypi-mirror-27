import logging

from prison import errors as e
from prison.apiutils import ok
from prison.client.card import is_can_play, play, cheat, finish
from prison.utils.card import (DO_NOT_CHANGE,
                               CHANGE_ANY, CHANGE_LEFT, which_change)
from prison.views import View, route

logger = logging.getLogger(__name__)


class CardView(View):
    @route("/v1/card", methods=["GET"])
    def _is_can_play(self):
        user_id, auth_key = self.auth_data
        return ok({
            "available": is_can_play(user_id, auth_key)
        })

    def _parse_cheat(self, cheat):
        return str(cheat).lower() not in ["false", "0"]

    @route("/v1/card", methods=["POST"])
    def _play_full_game(self):
        user_id, auth_key = self.auth_data
        _cheat = self._parse_cheat(self.args.get("cheat", False))
        wanna = self.args.get("wanna", "aa").lower()

        if not is_can_play(user_id, auth_key):
            raise e.ApiException(e.CARD_GAME_NOT_AVAILABLE)

        result = play(user_id, auth_key)
        if result is None:
            raise e.ApiException(e.CARD_GAME_PLAY_ERROR)

        if _cheat:
            while True:
                if not result or result["cheats"] == 0:
                    break

                card = which_change(
                    left=result["left"],
                    right=result["right"],
                    wanna=wanna,
                )
                if card == DO_NOT_CHANGE:
                    break

                if card == CHANGE_LEFT or card == CHANGE_ANY:
                    card = 'l'
                else:
                    card = 'r'

                result = cheat(user_id, auth_key, card)

        result = finish(user_id, auth_key)
        if result is None:
            raise e.ApiException(e.CARD_GAME_PLAY_ERROR)

        return ok(rewards=result)
