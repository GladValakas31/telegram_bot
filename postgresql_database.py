import psycopg2
from psycopg2 import OperationalError
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

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
        print("Подключение к БД осуществлено успешно")
    except OperationalError:
        print("Произошла ошибка OperationalError")
    return connection


connection = create_connection('postgres', DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)


def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("БД успешно создалась")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

create_database_query = "CREATE DATABASE student"
create_database(connection, create_database_query)

connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Запрос query выполнен успешно")
    except OperationalError:
        print("Произошла ошибка")

create_users_table = f"""
CREATE TABLE IF NOT EXISTS {DB_NAME} (
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
