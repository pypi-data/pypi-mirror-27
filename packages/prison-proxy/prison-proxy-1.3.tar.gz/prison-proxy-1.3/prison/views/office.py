import logging

from prison.apiutils import ok
from prison.client.office import get_cigarettes_count, take_cigarettes
from prison.views import View, route

logger = logging.getLogger(__name__)


class OfficeView(View):
    @route("/v1/office", methods=["GET"])
    def get_count_of_cigarettes(self):
        user_id, auth_key = self.auth_data
        return ok({
            "available": get_cigarettes_count(user_id, auth_key)
        })

    @route("/v1/office", methods=["POST"])
    def collect_cigarettes(self):
        user_id, auth_key = self.auth_data
        result, money = take_cigarettes(user_id, auth_key, all=True)
        return ok({
            "ok": result,
            "money": money
        })
