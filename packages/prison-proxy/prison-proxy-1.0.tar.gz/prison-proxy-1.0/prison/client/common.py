import json

import xmltodict

from prison.client import call_api


def collect_daily_bonus(user_id, auth_key):
    result = call_api("dailyBonus.claim", user_id=user_id, auth_key=auth_key)
    _json = json.loads(result)
    return _json["code"] == 0


def collect_toilet_paper(user_id, auth_key):
    result = call_api("collectToiletPaper", user_id=user_id, auth_key=auth_key)
    return "<msg>ok</msg>" in result


def duel_with_user(user_id, auth_key, enemy):
    result = call_api("challengeToDuel",
                      user_id=user_id,
                      auth_key=auth_key,
                      body={
                          "enemy": enemy
                      })
    # TODO: api returns info about money
    return "<win>1</win>" in result


def vote_for_friend(action, user_id, auth_key, friend_id):
    result = call_api("voteForFriend",
                      user_id=user_id,
                      auth_key=auth_key,
                      body={
                          "vote": action,
                          "sex": 0,
                          "model_id": 1,
                          "friend_uid": friend_id
                      })
    return "success vote" in result


def vote_positive_for_friend(user_id, auth_key, friend_id):
    return vote_for_friend(5, user_id, auth_key, friend_id)


def vote_negative_for_friend(user_id, auth_key, friend_id):
    return vote_for_friend(2, user_id, auth_key, friend_id)


def get_user_info(user_id, auth_key):
    data = call_api("getInfo", user_id=user_id, auth_key=auth_key)
    return xmltodict.parse(data)["data"]


def shave(user_id, auth_key):
    answer = call_api("shaveBeard", user_id=user_id, auth_key=auth_key)
    return '<code>0</code>' in answer
