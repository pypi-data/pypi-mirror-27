import logging

from prison.apiutils import ok
from prison.client.tasks import complete_tasks, get_tasks, is_tasks_done
from prison.views import View, route

logger = logging.getLogger(__name__)


class TaskView(View):
    @route("/v1/tasks", methods=["GET"])
    def _get_tasks(self):
        user_id, auth_key = self.auth_data
        return ok({
            "done": is_tasks_done(user_id, auth_key),
            "tasks": get_tasks(user_id, auth_key),
        })

    @route("/v1/tasks", methods=["POST"])
    def _complete_tasks(self):
        user_id, auth_key = self.auth_data

        result = complete_tasks(user_id, auth_key)
        return ok(result)
