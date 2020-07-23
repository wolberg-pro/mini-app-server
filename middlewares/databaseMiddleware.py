from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from common.database import create_database_connection


def registerDatabaseMiddleware(application: FastAPI):
    app_config = application.config
    session, dsn = create_database_connection(app_config)
    app_config.database.dsn = dsn

    async def db_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            request.state.db = session()
            response = await call_next(request)
        finally:
            request.state.db.rollback()
            request.state.db.close()
        return response

    writeLog(application, 'info', 'Register Database Middleware')
    return db_session_middleware
