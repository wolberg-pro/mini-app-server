from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from common.bootstrap import writeLog
from config.settings import settings


def registerConfigMiddleware(application: FastAPI):
    if settings.secret is None:
        raise RuntimeError('You have to set secret in the config module')

    application.config = settings

    async def settings_add_app(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            request.state.config = settings
            response = await call_next(request)
        finally:
            pass
        return response

    writeLog('info', 'Register Config Middleware')
    return settings_add_app
