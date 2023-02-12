from os import getenv
import setenv


PROJECT_NAME = getenv('PROJECT_NAME')
VERSION = getenv('VERSION')
API_PREFIX = getenv('API_PREFIX')
DEBUG = getenv('DEBUG')

DB_NAME = getenv('DB_NAME')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
POSTGRES_SCHEME = getenv('POSTGRES_SCHEME')


