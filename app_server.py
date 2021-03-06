#!/usr/bin/env python3
# coding=utf8
"""
Author: 归根落叶
Blog: https://www.bstester.com
"""

from tornado import httpserver, ioloop
from tornado.options import options, define
from tornado.web import Application
from includes.scheduler import job_monitor
from config import urls
from config import app as app_cfg
from config.db import init_db


class AppServer(Application):
    """应用启动入口"""
    def __init__(self):
        handlers = urls.handlers
        settings = {'template_path': app_cfg.template_path,
                    'static_path': app_cfg.static_path,
                    'cookie_secret': app_cfg.cookie_secret,
                    'xsrf_cookie': app_cfg.xsrf_cookie,
                    'login_url': app_cfg.login_url,
                    'ui_modules': app_cfg.ui_modules,
                    'debug': app_cfg.debug}
        Application.__init__(self, handlers, **settings)


def main():
    define('port', default=app_cfg.app_port, help='run on the given port', type=int)
    define('monitor', default='off', help='open jobs monitor', type=str)

    options.parse_command_line()
    http_server = httpserver.HTTPServer(AppServer(), xheaders=True)
    http_server.listen(options.port)
    if options.monitor.lower() == 'on':
        ioloop.PeriodicCallback(job_monitor, app_cfg.cycle_time * 1000).start()
    ioloop.IOLoop.instance().run_sync(init_db)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
