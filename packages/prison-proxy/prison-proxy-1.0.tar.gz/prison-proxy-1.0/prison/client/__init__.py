import random

import requests

AVAILABLE_SERVERS = [
    "http://109.234.156.250",
    "http://109.234.156.251",
    "http://109.234.156.252",
    "http://109.234.156.253",
]


def take_server():
    return random.choice(AVAILABLE_SERVERS)


def call_api(method, user_id, auth_key, body=None):
    if not body:
        body = dict()
    if "method" not in body:
        body["method"] = method
    if "user" not in body:
        body["user"] = user_id
    if "key" not in body:
        body["key"] = auth_key

    url = take_server() + "/prison/universal.php?" + method
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) " + \
                      "AppleWebKit/537.36 (KHTML, like Gecko) " + \
                      "Chrome/49.0.2623.110 Safari/537.36"
    }
    return requests.post(url, body, headers=headers).text
