import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from common.bootstrap import getApplication, loadCordsMiddleware, bindLogs, registerLogger, writeLog, settings
from middlewares.configMiddleware import registerConfigMiddleware
from middlewares.databaseMiddleware import registerDatabaseMiddleware
from middlewares.loggerMiddeware import registerLoggerMiddleware

application = getApplication()
application = loadCordsMiddleware()
enableLogs = False
logger = None
if settings.logs.enable:
    enableLogs = True
    bindLogs()
    registerLogger(__name__)
    writeLog('info', 'Server Logs Start')
'''Load middlewares'''
application.middleware('http')(registerLoggerMiddleware(application))
application.middleware('http')(registerConfigMiddleware(application))
application.middleware('http')(registerDatabaseMiddleware(application))


@application.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({'status': False, 'error': str(exc), 'code': 400}, status_code=400)


if __name__ == "__main__":
    writeLog('info', 'Server Binding Process start')
    isDebugMode = False
    try:
        isDebugMode = settings.debug
        writeLog('info', 'Server Debug mode enabled')
    except NameError:
        print("Server debug mode is offline")
    if isDebugMode:
        uvicorn.run(app=application, host="0.0.0.0", port=settings.port, log_level=settings.logs.level, reload=True,
                    debug=True)
    else:
        uvicorn.run(app=application, host="0.0.0.0", port=settings.port, log_level=settings.logs.level, reload=False)
