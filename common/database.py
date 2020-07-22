from config.settings import Settings


def get_database_dns(settings: Settings):
    return '{type}://{username}:{password}@{host}:{port}/{database}'.format(
        settings.database.type, settings.username, settings.password, settings.host, settings.port,
        settings.database.database
    )


def create_database_connection(settings: Settings):
    SQLALCHEMY_DATABASE_URI = get_database_dns(settings)
