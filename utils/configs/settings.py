"""Load in the .env credentials once so they are all accessible"""
from os import path, getenv
from dotenv import load_dotenv

# import project paths to export
PROJECT_FOLDER = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
print('PROJECT_FOLDER:', PROJECT_FOLDER)
ENV_PATH = PROJECT_FOLDER + '/.env'
LOGS_FILE_PATH = PROJECT_FOLDER + '/logs/history.csv'

# set of files to allow to be uploaded
# ALLOWED_EXTENSIONS = {'csv'}

# set environment path for environment variables
load_dotenv(ENV_PATH)

# variables to export:

# database level info
DB_USERNAME = getenv('DB_USERNAME')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_DATABASE = getenv('DB_DATABASE')
DB_HOST = getenv('DB_HOST')
DB_TABLE = getenv('DB_TABLE')
# DB_COLUMN_DETAIL_TABLE = getenv('DB_COLUMN_TABLE')

# server level info
PORT = int(getenv('PORT'))
IS_TEST_INSTANCE = getenv('IS_TEST_INSTANCE')

# server authentication items
# SERVER_USERNAME = getenv('SERVER_USERNAME')
# SERVER_PASSWORD = getenv('SERVER_PASSWORD')


# if a query attempts any of these, don't allow
# FORBIDDEN_OPERATIONS = ['DROP', 'DELETE', 'ALTER', 'UPDATE', 'INSERT', 'CREATE']

# ALLOWED_EXTRACTION_FILE_FORMATS = {'csv', 'xlsx'}


# database field type groups:
DATE_FIELD_DATA_TYPES = {'date', 'datetime'}
NUMBER_FIELD_DATA_TYPES = {'tinyint', 'int', 'double'}
