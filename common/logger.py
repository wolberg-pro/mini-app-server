import logging
import sys

from pythonjsonlogger import jsonlogger  # pip install python-json-logger
from starlette_context import context

from config.settings import settings

if settings.logs_enable:
    logging.config.fileConfig('config/logging.conf')
    if settings.logs_json_enable:
        formatter = jsonlogger.JsonFormatter()
        logging.setFormatter(formatter)


class MyApiLoggingAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        if extra is None:
            extra = {}
        super(MyApiLoggingAdapter, self).__init__(logger, extra)

    def process(self, msg, kwargs):
        extra = self.extra.copy()
        extra.update(context.data)  # <----  here we are basically adding context to log
        kwargs["extra"] = extra
        return msg, kwargs

def getLogger(name):
    return MyApiLoggingAdapter(logging.getLogger(name))