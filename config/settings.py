from pydantic import BaseSettings


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
    database_type: str = 'postgresql'
    database_host: str = '127.0.0.1'
    database_port: int = 5432
    database_name: str = 'miniapp'
    database_user: str = 'postgres'
    database_password: str = 'postgres'
    logs_enable: bool = True
    logs_level: str = 'debug'
    logs_enable_sentry: bool
    logs_sentry_dns: str
    cords_enable: bool = True
    cords_domains: []
    cords_methods: ['GET', 'PUT', 'POST', 'DELETE']
    cords_headers: ["*"]
    meta_pageSizeDef: int = 50
    meta_pageSizes = [10, 20, 30, 50, 100, 200]

    class Config:
        env_file: str = '.env'


settings = Settings()
