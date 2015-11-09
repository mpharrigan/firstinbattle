import logging
import tornado.ioloop
import tornado.web
from pkg_resources import resource_filename
from tornado.web import Application, StaticFileHandler
from .gofish import GoFishRh, GoFishWs
from collections import defaultdict

log = logging.getLogger(__name__)


class AngularHandler(StaticFileHandler):
    def initialize(self, *args, **kwargs):
        path = resource_filename(__name__, "app/")
        log.debug("Serving static app files from {}".format(path))
        super().initialize(path)


class FIBApplication(Application):
    @classmethod
    def _get_handlers(cls):
        return [
            (r"/app/(.*)", AngularHandler),
            (r"/gofish/(.*)", GoFishRh),
            (r"/gofish-ws", GoFishWs)
        ]

    def __init__(self):
        self.games = defaultdict(list)

        super().__init__(
            self._get_handlers(),
            template_path=resource_filename(__name__, 'templates/'),
            static_path=resource_filename(__name__, 'static/'),
            debug=False,
        )


def main():
    logging.basicConfig(level=logging.DEBUG)
    port = 7777
    log.info("Listening on port %d", port)
    FIBApplication().listen(port)
    tornado.ioloop.IOLoop.instance().start()
