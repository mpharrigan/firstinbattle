import logging
import os
from collections import defaultdict

import tornado.ioloop
import tornado.web
import tornado.wsgi
from pkg_resources import resource_filename
from tornado.web import Application, StaticFileHandler

from .gofish import GoFishRh, GoFishWs

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
        self.users = dict()

        super().__init__(
            self._get_handlers(),
            template_path=resource_filename(__name__, 'templates/'),
            static_path=resource_filename(__name__, 'static/'),
            debug=False,
            cookie_secret="oooh--secret",
        )


def main():
    logging.basicConfig(level=logging.DEBUG)
    port = int(os.environ.get("PORT", 7777))
    log.info("Listening on port %d", port)
    FIBApplication().listen(port)
    tornado.ioloop.IOLoop.instance().start()


application = FIBApplication()
wsgi_app = tornado.wsgi.WSGIAdapter(application)
