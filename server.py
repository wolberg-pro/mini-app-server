import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from common.bootstrap import getApplication, loadCordsMiddleware, settings
application = getApplication()
application = loadCordsMiddleware()
@application.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({ 'status': False,  'error':  str(exc), 'code': 400}, status_code=400)

if __name__ == "__main__":
    isDebugMode = False
    try:
        isDebugMode = settings.debug
    except NameError:
        print("Server debug mode is offline")
    if isDebugMode:
        uvicorn.run(app=application, host="0.0.0.0", port=settings.port, log_level=settings.logs.level, reload=True, debug=True)
    else:
        uvicorn.run(app=application, host="0.0.0.0", port=settings.port, log_level=settings.logs.level, reload=False)

