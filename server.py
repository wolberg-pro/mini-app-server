import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pprint import pprint
from common.bootstrap import getApplication, loadCordsMiddleware, bindLogs, registerLogger, writeLog, settings
from middlewares.configMiddleware import registerConfigMiddleware
from middlewares.databaseMiddleware import registerDatabaseMiddleware
from middlewares.loggerMiddeware import registerLoggerMiddleware
from routes.routes import router

print("Starting Server")
application = getApplication()
pprint(f"Server Start With Config({vars(settings)})")
application = loadCordsMiddleware(application)
enableLogs = False
logger = None
if settings.logs_enable:
    enableLogs = True
    bindLogs()
    registerLogger(application, __name__)
    writeLog(application, 'info', 'Server Logs Start')
'''Load middlewares'''
if enableLogs:
    application.middleware('http')(registerLoggerMiddleware(application))
application.middleware('http')(registerConfigMiddleware(application))
# application.middleware('http')(registerDatabaseMiddleware(application))

application.include_router(router)


@application.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({'status': False, 'error': str(exc), 'code': 400}, status_code=400)


if __name__ == "__main__":
    writeLog(application, 'info', 'Server Binding Process start')
    isDebugMode = False
    try:
        isDebugMode = settings.debug
        writeLog(application, 'info', 'Server Debug mode enabled')
    except NameError:
        print("Server debug mode is offline")
    if isDebugMode:
        uvicorn.run(app=application, host="0.0.0.0", port=settings.port, log_level=settings.logs_level, reload=True,
                    debug=True, workers=settings.workers)
    else:
        uvicorn.run(app=application, host="0.0.0.0", port=settings.port, log_level=settings.logs_level, reload=False,
                    workers=settings.workers)
