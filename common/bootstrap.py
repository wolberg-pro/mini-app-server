import logging
from functools import lru_cache
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from config.settings import settings

active_logger = None


def getApplication():
    application = FastAPI(title=settings.appName,
                          description=settings.description,
                          debug=settings.debug)

    return application


@lru_cache()
def getConfig():
    return settings


def bindLogs():
    logging.config.fileConfig('config/logging.conf')


def registerLogger(application: FastAPI, name: str):
    if settings.logs_enable:
        application.logger = logging.getLogger(name)
    pass


def writeLog(application: FastAPI, callable_method: str, message: object, **args) -> object:
    """
    wrtie log by call method name and call the logger object
    :param callable_method: method name
    :param message: log message
    :param args: args to logs
    """
    if settings.logs_enable:
        if len(args) == 0:
            getattr(application.logger, callable_method)(message)
        else:
            getattr(application.logger, callable_method)(message, args)
    else:
        print(message, args)


def loadCordsMiddleware(application: FastAPI):
    if settings.cords_enable:
        application.add_middleware(CORSMiddleware,
                                   allow_origins=settings.cords_origins,
                                   allow_credentials=True,
                                   allow_methods=settings.cords_methods,
                                   allow_headers=settings.cords_headers)
    return application
