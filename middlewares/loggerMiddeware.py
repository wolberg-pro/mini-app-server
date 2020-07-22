from datetime import time
from server import application
from common.bootstrap import registerLogger, writeLog
from fastapi.requests import Request

def registerLoggerMiddleware():
    @application.middleware('http')
    async def logMiddlewareHandler(request: Request, call_next):
        registerLogger(__name__)
        writeLog('info', f"request path: {request.path} , method: {request.method} , data: {request.data}")
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        writeLog('info', f"completed_in={formatted_process_time}ms status_code={response.status_code}")
        return response
