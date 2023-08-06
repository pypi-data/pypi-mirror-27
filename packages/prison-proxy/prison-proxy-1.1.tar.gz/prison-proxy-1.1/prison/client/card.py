import logging

import xmltodict

from prison.client import call_api

logger = logging.getLogger(__name__)


def is_can_play(user_id, auth_key):
    result = call_api("cardGameInit", user_id=user_id, auth_key=auth_key)
    return "<canPlay>1</canPlay>" in result


def play(user_id, auth_key):
    answer = call_api("cardGamePlay", user_id=user_id, auth_key=auth_key)
    if "<result>0</result>" not in answer:
        logger.error(answer)
        return

    xml = xmltodict.parse(answer)
    return {
        "id": int(xml["data"]["gameCount"]),
        "left": str(xml["data"]["game"]["cardLeft"]),
        "right": str(xml["data"]["game"]["cardRight"]),
        "cheats": int(xml["data"]["game"]["cheatsLeft"]),
    }


def finish(user_id, auth_key):
    answer = call_api("cardGameFinish", user_id=user_id, auth_key=auth_key)
    if "<result>0</result>" not in answer:
        logger.error(answer)
        return

    rewards = []
    xml = xmltodict.parse(answer)
    for reward in xml["data"]["rewards"]["reward"]:
        rewards.append({
            "type": reward["@type"],
            "value": reward["#text"],
        })
    return rewards
