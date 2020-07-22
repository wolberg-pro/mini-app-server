from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import Settings


def get_database_dns(settings: Settings):
    return '{type}://{username}:{password}@{host}:{port}/{database}'.format(
        settings.database.type, settings.username, settings.password, settings.host, settings.port,
        settings.database.database
    )


def create_database_connection(settings: Settings):
    dsn = get_database_dns(settings)
    engine = create_engine(dsn)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session, dsn
