import time
from fastapi import FastAPI
from common.bootstrap import registerLogger, writeLog
from fastapi.requests import Request

def registerLoggerMiddleware(application: FastAPI):
    registerLogger(application,__name__)
    async def logMiddlewareHandler(request: Request, call_next):
        writeLog(application, 'info', f"request path: {request.url} , method: {request.method}")
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}s'.format(process_time)
        writeLog(application, 'info', f"completed_in={formatted_process_time}ms status_code={response.status_code}")
        return response

    writeLog(application, 'info', 'Register Logger Middleware')
    return logMiddlewareHandler
