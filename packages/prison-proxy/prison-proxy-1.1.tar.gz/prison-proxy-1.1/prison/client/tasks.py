import logging

import xmltodict

from prison.client import call_api
from prison.client.common import send_presents, vote_negative_for_friend
from prison.client.office import take_cigarettes

logger = logging.getLogger(__name__)

DONE_ALL = 0
SEND_PRESENT = 1
DO_SPIT = 2
GOT_OFFICE = 5
GOT_RESPECT = 10


def get_tasks(user_id, auth_key):
    answer = call_api("getUsersTasks", user_id=user_id, auth_key=auth_key)
    tasks = xmltodict.parse(answer)
    result = []
    for job in tasks["data"]["jobs"]["job"]:
        result.append({
            "id": int(job["id"]),
            "amount": int(job["amount"]),
            "count": int(job.get("count", 0)),
        })
    return result


def _send_presents(user_id, auth_key):
    recipients = [
        "1",
        "5181546",
        "6140565",
        "6637770",
        "130006452",
        "257532842",
    ]
    # TODO: analyze result
    result = send_presents(user_id, auth_key, recipients)


def _spit(user_id, auth_key):
    # TODO: analyze resultX
    result1 = vote_negative_for_friend(1, user_id, auth_key)
    result2 = vote_negative_for_friend(130006452, user_id, auth_key)
    result3 = vote_negative_for_friend(257532842, user_id, auth_key)
    result4 = vote_negative_for_friend(5181546, user_id, auth_key)
    result5 = vote_negative_for_friend(6140565, user_id, auth_key)


def _collect_office(user_id, auth_key):
    # TODO: analyze result
    result, money = take_cigarettes(user_id, auth_key, all=True)


def is_tasks_done(user_id, auth_key):
    return _is_tasks_done(tasks=get_tasks(user_id, auth_key))


def _is_tasks_done(tasks):
    for task in tasks:
        if task["id"] == DONE_ALL and task["count"] == task["amount"]:
            return True
    return False


def complete_tasks(user_id, auth_key):
    tasks = get_tasks(user_id, auth_key)
    if _is_tasks_done(tasks):
        return True

    for task in tasks:
        if task["id"] == SEND_PRESENT:
            _send_presents(user_id, auth_key)
            continue

        if task["id"] == DO_SPIT:
            _spit(user_id, auth_key)
            continue

        if task["id"] == GOT_RESPECT:
            # do action?
            continue

        if task["id"] == GOT_OFFICE:
            _collect_office(user_id, auth_key)
            continue

        logging.warning("new task: {}".format(task))

    return _is_tasks_done(tasks=get_tasks(user_id, auth_key))
