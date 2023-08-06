# coding=utf-8
import xmltodict

from prison.client import call_api


def get_cities(user_id, auth_key):
    answer = call_api("getCities", user_id=user_id, auth_key=auth_key)
    xml = xmltodict.parse(answer)
    return xml["data"]["cities"]["city"]


def do_city_action(user_id, auth_key, city, action_id):
    result = call_api("doCityAction",
                      user_id=user_id,
                      auth_key=auth_key,
                      body={
                          "city": city,
                          "action_id": action_id,
                          "action_type": 3
                      })
    xml = xmltodict.parse(result)
    if xml["data"].get("energy"):
        return int(xml["data"]["energy"])
    return 0


def get_city_info(user_id, auth_key, city):
    answer = call_api("getCityInfo",
                      user_id=user_id,
                      auth_key=auth_key,
                      body={
                          "city": city
                      })
    info = xmltodict.parse(answer)
    return info["data"]


def complete_city(user_id, auth_key, city, night=False):
    info = get_city_info(user_id, auth_key, city)
    done_missions = 0
    for mission in info["missions"]["mission"]:
        # Необходимо найти невыполненное задание.
        # (количество тиков < максимального кол-ва тиков)
        complete_tick = int(mission["completeTick"])
        all_tick = int(mission["allTick"])
        if complete_tick >= all_tick:
            continue

        action_id = int(mission["id"])

        # Проверка на выполнение ночных ходок
        if action_id >= 8 and not night:
            # Выходим из цикла, если
            # мы закончили дневные задания и остались
            # только ночные задания, а их проходить не нужно.
            break

        need_energy = int(mission["necessaryEnergy"])
        for i in range(complete_tick, all_tick):
            # TODO: Обрабатывать ответ. Возможны нычки
            # <new_collection_element><cid>39</cid><id>6</id></new_collection_element>
            energy = do_city_action(user_id, auth_key, city, action_id)
            # case: закончилась энергия
            if energy < need_energy:
                return


def collect_building_rewards(user_id, auth_key):
    answer = call_api("getAllBuildingsRewards",
                      user_id=user_id,
                      auth_key=auth_key)
    xml = xmltodict.parse(answer)
    return {
        "timetoprofit": int(xml["data"]["timetoprofit"]),
        "money": int(xml["data"]["money"]),
        "rating": int(xml["data"]["rating"]),
        "love": int(xml["data"]["love"]),
    }
