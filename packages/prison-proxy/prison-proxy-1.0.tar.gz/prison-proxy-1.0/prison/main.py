import logging

from flask import Flask

from prison.apiutils import ApiDecorator
from prison.views import init_view
from prison.views.card import CardView
from prison.views.city import CityView
from prison.views.common import CommonView
from prison.views.office import OfficeView
from prison.views.slot import SlotView

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")


def create_app(global_conf, **local_conf):
    app = Flask(__name__)
    decorator = ApiDecorator()
    for cls in [
        CardView,
        CityView,
        CommonView,
        OfficeView,
        SlotView,
    ]:
        init_view(view_cls=cls, app=app, decorator=decorator)
    return app


if __name__ == "__main__":
    app = create_app({})
    app.run("127.0.0.1", 2018, debug=True)
