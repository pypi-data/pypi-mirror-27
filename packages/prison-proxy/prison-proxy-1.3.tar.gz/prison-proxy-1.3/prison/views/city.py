import logging

from prison.apiutils import ok
from prison.client.city import (collect_building_rewards,
                                get_cities,
                                get_city_info,
                                complete_city)
from prison.views import View, route

logger = logging.getLogger(__name__)


class CityView(View):
    @route("/v1/city", methods=["GET"])
    def _get_cities(self):
        user_id, auth_key = self.auth_data
        return ok(ok=get_cities(
            user_id=user_id,
            auth_key=auth_key,
        ))

    @route("/v1/city/<city>", methods=["GET"])
    def _get_city_info(self, city):
        user_id, auth_key = self.auth_data
        return ok(ok=get_city_info(
            user_id=user_id,
            auth_key=auth_key,
            city=city
        ))

    @route("/v1/city/<city>", methods=["POST"])
    def _complete_city(self, city):
        user_id, auth_key = self.auth_data
        complete_city(
            user_id=user_id,
            auth_key=auth_key,
            city=city
        )
        return ok()

    @route("/v1/city/<city>/night", methods=["POST"])
    def _complete_city_night(self, city):
        user_id, auth_key = self.auth_data
        return ok(ok=complete_city(
            user_id=user_id,
            auth_key=auth_key,
            city=city,
            night=True
        ))

    @route("/v1/city/rewards", methods=["POST"])
    def _collect_building_rewards(self):
        user_id, auth_key = self.auth_data
        return ok(collect_building_rewards(
            user_id=user_id,
            auth_key=auth_key,
        ))
