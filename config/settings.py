from pydantic import BaseSettings


class DatabaseSettings:
    type: str = 'postgresql'
    host: str = '127.0.0.1'
    port: int = 5432
    database: str = 'miniapp'
    user: str = 'postgres'
    password: str = 'postgres'


class LogsSettigns:
    enable: bool = True
    level: str = 'debug'
    enable_sentry: bool
    sentry_dns: str


class MetaSettings:
    pageSizeDef: int = 50
    pageSizes = [10, 20, 30, 50, 100, 200]


class CordsSettings:
    enable: bool = True
    domains: []
    methods: ['GET', 'PUT', 'POST', 'DELETE']
    headers: ['*']


class Settings(BaseSettings):
    appName: str = 'Mini App'
    version: str = '1.0.1'
    description: str = 'Mini Application Mini Shop writing with react/react native'
    debug: bool = True
    prefixAPI: str = 'api'
    host: str = '0.0.0.0'
    port: int = 5700
    secret: str = '4t32fvg78^&*gbh54by_b45n6^&23#try!'
    workers: int = 1
    database: DatabaseSettings
    logs: LogsSettigns
    cords: CordsSettings
    meta: MetaSettings

    class Config:
        env_file: str = '.env'


settings = Settings()
