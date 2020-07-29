from pprint import pprint
import uvicorn
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware
from common.bootstrap import getApplication, loadCordsMiddleware,  registerLogger, writeLog, settings
from middlewares.configMiddleware import registerConfigMiddleware
from middlewares.loggerMiddeware import registerLoggerMiddleware
from routes.routes import router


class Application:
    def __init__(self):
        print("Starting Server")
        self.applicationObject = getApplication()
        pprint(f"Server Start With Config({vars(settings)})")
        self.applicationObject.include_router(router)

    def __startLogSystem(self):
        enableLogs = False
        if settings.logs_enable:
            enableLogs = True
            registerLogger(self.applicationObject, __name__)
            writeLog(self.applicationObject, 'info', 'Server Logs Start')
        return enableLogs

    def __registerMiddleWares(self):
        application = loadCordsMiddleware(self.applicationObject)
        '''Load middlewares'''
        if self.__startLogSystem():
            application.middleware('http')(registerLoggerMiddleware(self.applicationObject))
        application.middleware('http')(registerConfigMiddleware(self.applicationObject))
        application.add_middleware(ContextMiddleware.with_plugins(
            plugins.CorrelationIdPlugin(),
            plugins.RequestIdPlugin(),
            plugins.DateHeaderPlugin(),
            plugins.ForwardedForPlugin(),
            plugins.UserAgentPlugin(),
        ))
        # application.middleware('http')(registerDatabaseMiddleware(self.applicationObject))

    async def __onApplicationStart(self):
        pass

    async def __onApplicationStop(self):
        pass

    def __bindEvents(self):
        @self.applicationObject.on_event("startup")
        async def startup():
            await self.__onApplicationStart()

        @self.applicationObject.on_event("shutdown")
        async def shutdown():
            await self.__onApplicationStop()

        @self.applicationObject.exception_handler(RequestValidationError)
        async def validation_exception_handler(request, traceback):
            print(traceback.print_exc())
            return JSONResponse({'status': False, 'error': str(traceback), 'code': 400}, status_code=400)

    def __bindServerPackages(self,name:str):
        writeLog(self.applicationObject, 'info', 'Server Binding Process start')
        if name == "__main__":
            isDebugMode = False
            try:
                isDebugMode = settings.debug
                writeLog(self.applicationObject, 'info', 'Server Debug mode enabled')
            except NameError:
                print("Server debug mode is offline")
            uvicorn.run("server:application",
                        host="0.0.0.0",
                        port=settings.port,
                        log_level=settings.logs_level,
                        reload=isDebugMode,
                        debug=isDebugMode)
    def getApplication(self):
        return self.applicationObject
    def run(self , name):
        self.__registerMiddleWares()
        self.__bindEvents()
        self.__bindServerPackages(name)

