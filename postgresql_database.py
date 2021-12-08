import psycopg2
from psycopg2 import OperationalError
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    filename='logger.log'
)

logger = logging.getLogger(__name__)

def create_connection(db_name, db_user, db_password, db_host, db_port):

    """Функция, осуществляющая подключение к базе данных"""

    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        logger.info('Connection to the database was successful')
    except OperationalError:
        logger.error('An OperationalError occurred')
    return connection


connection = create_connection('postgres', DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
logger.info('The connection to the database was successful')


def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        logger.info('The database was created successfully')
    except OperationalError:
        logger.error('An OperationalError occurred')

create_database_query = "CREATE DATABASE student"
create_database(connection, create_database_query)

connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
logger.info('The connection to the database was successful')

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logger.info('Query completed successfully')
    except OperationalError:
        logger.error('An OperationalError occurred')

create_users_table = """
CREATE TABLE IF NOT EXISTS students (
  fam character(20) NOT NULL,
  name character(20) NOT NULL,
  patronymic character(20) NOT NULL,
  grp character(20) NOT NULL,
  var character(20) NOT NULL,
  git character(100) NOT NULL,
  res boolean NOT NULL
)
"""

execute_query(connection, create_users_table)
