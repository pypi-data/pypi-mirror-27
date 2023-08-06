import xmltodict

from prison.client import call_api


def get_cigarettes_count(user_id, auth_key):
    result = call_api("office", user_id=user_id, auth_key=auth_key)
    xml = xmltodict.parse(result)
    return int(xml["data"]["ideascount"])


def take_cigarettes(user_id, auth_key, all=False):
    result = call_api("office",
                      user_id=user_id,
                      auth_key=auth_key,
                      body={
                          "getidea": 5 if all else 1
                      })
    xml = xmltodict.parse(result)
    return int(xml["data"]["result"]) == 1, int(xml["data"]["money"])
