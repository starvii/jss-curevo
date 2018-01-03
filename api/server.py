#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import ioloop
from tornado import options
from tornado import httpserver
from tornado.options import define, options
from app import app
from method.logger import default_logger as log

define('port', default=80, help='run on the given port', type=int)
define('debug', default=True, help='debug mode', type=bool)


def start_server():
    options.parse_command_line()
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port, address='127.0.0.1')

    log.info('Development server is running at http://127.0.0.1:%s' % options.port)
    log.info('Quit the server with Control-C')

    ioloop.PeriodicCallback(app.backend.cleanup_session, 60000)
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    start_server()
