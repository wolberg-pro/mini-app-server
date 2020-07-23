from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import Settings


def get_database_dns(settings: Settings):
    return '{database_type}://{database_username}:{database_password}@{database_host}:{database_port}/{database_name}'.format(
        **settings
    )


def create_database_connection(settings: Settings):
    dsn = get_database_dns(settings)
    engine = create_engine(dsn)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session, dsn
