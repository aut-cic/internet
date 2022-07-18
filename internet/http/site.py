import sanic
from sanic_ext import render

from ..message.message import MESSAGES


class SiteHandler():
    @staticmethod
    async def index(_: sanic.Request) -> sanic.HTTPResponse:
        return await render(
            "index.html", context={
                'messages': MESSAGES,
            }, status=200
        )
 
    def register(self) -> sanic.Blueprint:
        bp = sanic.Blueprint("site", url_prefix='/')
        bp.add_route(self.index, '/', methods=['GET'])

        return bp
