import logging
from functools import lru_cache
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from config.settings import settings

active_logger = None

def getApplication():
    application = FastAPI(title=settings.appName,
                          description=settings.description,
                          version=settings.prefixAPI,
                          debug=settings.debug)
    application.include_router(
        api_router, prefix=settings.prefixAPI)

    return application


@lru_cache()
def getConfig():
    return settings


def bindLogs():
    logging.config.fileConfig('config/logging.conf')


def registerLogger(name: str):
    if settings.logs.enable:
        active_logger = logging.getLogger(name)
    pass


def writeLog(callable_method: str, message: object, args: object) -> object:
    """
    wrtie log by call method name and call the logger object
    :param callable_method: method name
    :param message: log message
    :param args: args to logs
    """
    if settings.logs.enable:
        getattr(active_logger, callable_method)(message, args)
    else:
        print(message, args)


def loadCordsMiddleware(application: FastAPI):
    if settings.cords.enable:
        application.add_middleware(CORSMiddleware,
                                   allow_origins=settings.cords.origins,
                                   allow_credentials=True,
                                   allow_methods=settings.cords.methods,
                                   allow_headers=settings.cords.headers)
    return application
