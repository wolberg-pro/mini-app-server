import logging
from functools import lru_cache
from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from config.settings import settings


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


def loadCordsMiddleware(application: FastAPI):
    if settings.cords.enable:
        application.add_middleware(CORSMiddleware,
                                   allow_origins=settings.cords.origins,
                                   allow_credentials=True,
                                   allow_methods=settings.cords.methods,
                                   allow_headers=settings.cords.headers)
    return application