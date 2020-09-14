class Config(object):
    DEBUG = True
    TESTING = False
    DB_HOST = 'db'
    DB_USER = 'root'
    DB_PASS = 'admin1'
    DB_NAME = 'dbo'

class ProductionConfig(Config):
    DB_SERVER = 'spotify-mood-tracker.database.windows.net'
    DB_NAME = 'spotify-mood-tracker'
    DB_USER = 'adriandavid'
    DB_PASS = 'Mayllah11'
    DB_DRIVER= '{ODBC Driver 17 for SQL Server}'

class DevelopmentConfig(Config):
    DEBUG = True
