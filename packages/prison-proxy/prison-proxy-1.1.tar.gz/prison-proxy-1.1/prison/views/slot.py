import logging

from prison import errors as e
from prison.apiutils import ok
from prison.client.slot import get_slot_info, set_bet, spin, spin_all_energy
from prison.views import View, route

logger = logging.getLogger(__name__)


class SlotView(View):
    @route("/v1/slot", methods=["GET"])
    def _get_slot_info(self):
        user_id, auth_key = self.auth_data
        return ok(get_slot_info(user_id, auth_key))

    @route("/v1/slot", methods=["POST"])
    def _spin(self):
        user_id, auth_key = self.auth_data

        result = spin(user_id, auth_key)
        if result is None:
            raise e.ApiException(e.SLOT_PLAY_ERROR)
        return ok(result)

    @route("/v1/slot/all", methods=["POST"])
    def _spin_all(self):
        user_id, auth_key = self.auth_data

        result = spin_all_energy(user_id, auth_key)
        if result is None:
            raise e.ApiException(e.SLOT_PLAY_ERROR)
        return ok(result)

    @route("/v1/slot", methods=["PATCH"])
    def _set_bet(self):
        user_id, auth_key = self.auth_data
        if set_bet(user_id, auth_key, self.data["bet"]):
            return ok()
        raise e.ApiException(e.SLOT_BET_ERROR)
