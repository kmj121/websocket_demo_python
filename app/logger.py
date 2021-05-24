import json
import logging
import logging.handlers
import os
import re
import sys

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger

from config import config

"""
20190523
logs/log
test: logger_test
prod: logger_prod

local and info: default not send sentry
console: format str to json
log file: not format
"""


class MyFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)

    def formatMessage(self, record):
        try:
            s = json.loads(record.getMessage().replace("'", "\""))
            record.message = json.dumps(s, indent=True, ensure_ascii=False)
        except(TypeError, json.decoder.JSONDecodeError):
            record.message = record.getMessage()
            if getattr(config, "sessionId", None):
                record.message = config.__getattribute__("sessionId") + " " + record.message
        return self._style.format(record)

    def format(self, record):
        return self.get_pathname(self.get_nopwd(self.get_nobase64(super().format(record))))

    def get_nobase64(self, msg):
        return re.sub(r"('|\"|)[\w=+/]{100,}('|\"|)", r"\g<1>hidden\g<1>", msg)  # hidden base64 message

    def get_nopwd(self, msg):  # hidden password
        return re.sub("(pwd|password)(.*?:)(.*?)('|\"|)(,|})", r"\g<1>\g<2>\g<4>*\g<4>\g<5>", msg, flags=re.IGNORECASE)

    def get_pathname(self, msg):
        return re.sub(r"/[.\S]*/([.\S]*)/([.\S]*\.py) ", r"\g<1>/\g<2> ", msg)  # pathname


class Logs:
    PATH = os.path.join(os.path.dirname(sys.path[0]), "logs")
    LOG_INSTANCE = None
    config = None

    def __init__(self, *args):
        Logs.config = args[0].__dict__
        local_name, name = "logger_local", f"logger_{Logs.config.get('ENV', 'local')}"
        # if local_name != name:
        #     sentry_logging = LoggingIntegration(
        #         level=logging.WARNING,  # Capture info and above as breadcrumbs
        #         event_level=logging.WARNING  # Send errors as events
        #     )
        #     sentry_sdk.init(
        #         dsn=Logs.config.get('DSN', None),
        #         integrations=[sentry_logging]
        #     )
        # ignore_logger(local_name)  # except local
        Logs.LOG_INSTANCE = logging.getLogger(name)
        if not os.path.isdir(Logs.PATH):
            os.makedirs(Logs.PATH, 0o777, True)

        if not Logs.LOG_INSTANCE.handlers:
            fmt, datefmt = '%(asctime)s %(pathname)s [line:%(lineno)d] %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S'
            formatter = MyFormatter(fmt=fmt, datefmt=datefmt)

            console = logging.StreamHandler()
            console.setFormatter(formatter)
            Logs.LOG_INSTANCE.addHandler(console)

            handler = logging.handlers.TimedRotatingFileHandler(
                os.path.join(Logs.PATH, 'log'),
                when='MIDNIGHT',
                interval=1,
                backupCount=15,
                encoding="utf-8"
            )
            handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
            Logs.LOG_INSTANCE.addHandler(handler)

            Logs.LOG_INSTANCE.setLevel(logging.INFO)

            Logs.LOG_INSTANCE.warning({"启动参数": Logs.config})


LOG = Logs(config).LOG_INSTANCE
