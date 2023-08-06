import json
import logging

import xmltodict

from prison.client import call_api

logger = logging.getLogger(__name__)


def get_slot_info(user_id, auth_key):
    answer = call_api("getInfo", user_id=user_id, auth_key=auth_key)
    user_info = xmltodict.parse(answer)
    return {
        "bet": int(user_info["data"]["slotGame"]["game"]["bet"]),
        "energy": int(user_info["data"]["slotGame"]["energy"])
    }


def set_bet(user_id, auth_key, bet):
    answer = call_api("slotGame.setBet",
                      user_id=user_id,
                      auth_key=auth_key,
                      body={
                          "bet": bet
                      })

    if '"error":"ok"' in answer:
        return True
    logger.error(answer)
    return False


def spin(user_id, auth_key):
    answer = call_api("slotGame.spin", user_id=user_id, auth_key=auth_key)
    if '"code":0' not in answer:
        logging.error(answer)
        return

    result = json.loads(answer)
    return {
        "energy": result["pe"]["energy"],
        "rewards": result["rewards"],
    }


def spin_all_energy(user_id, auth_key):
    rewards = []
    last_energy = 0
    while True:
        result = spin(user_id, auth_key)
        if not result:
            break
        last_energy = result["energy"]
        rewards.extend(result["rewards"])

    if not rewards:
        return

    return {
        "rewards": rewards,
        "energy": last_energy,
    }
