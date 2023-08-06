import logging

from prison.apiutils import ok
from prison.client.common import (duel_with_user,
                                  collect_daily_bonus,
                                  collect_toilet_paper,
                                  vote_negative_for_friend,
                                  vote_positive_for_friend,
                                  shave)
from prison.views import View, route

logger = logging.getLogger(__name__)


class CommonView(View):
    @route("/v1/common/daily", methods=["POST"])
    def _collect_daily_bonus(self):
        user_id, auth_key = self.auth_data
        return ok(ok=collect_daily_bonus(
            user_id=user_id,
            auth_key=auth_key,
        ))

    @route("/v1/common/shave", methods=["POST"])
    def _shave(self):
        user_id, auth_key = self.auth_data
        return ok(ok=shave(
            user_id=user_id,
            auth_key=auth_key,
        ))

    @route("/v1/common/toilet", methods=["POST"])
    def _collect_toilet_paper(self):
        user_id, auth_key = self.auth_data
        return ok(ok=collect_toilet_paper(
            user_id=user_id,
            auth_key=auth_key,
        ))

    @route("/v1/common/fight", methods=["POST"])
    def _duel_with_user(self):
        user_id, auth_key = self.auth_data
        enemy = self.data["enemy"]
        return ok(ok=duel_with_user(
            user_id=user_id,
            auth_key=auth_key,
            enemy=enemy,
        ))

    @route("/v1/common/vote/positive", methods=["POST"])
    def _vote_positive(self):
        user_id, auth_key = self.auth_data
        friend_id = self.data["friend_id"]
        return ok(ok=vote_positive_for_friend(
            user_id=user_id,
            auth_key=auth_key,
            friend_id=friend_id,
        ))

    @route("/v1/common/vote/negative", methods=["POST"])
    def _vote_negative(self):
        user_id, auth_key = self.auth_data
        friend_id = self.data["friend_id"]
        return ok(ok=vote_negative_for_friend(
            user_id=user_id,
            auth_key=auth_key,
            friend_id=friend_id,
        ))
