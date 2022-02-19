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


def execute_query(query):
    """
    Функция, осуществляющая введение запроса в БД через переменную query.
    :param query: запрос в PostrgeSQL
    :return: None
    """
    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logger.info('The database was created successfully')
    except OperationalError:
        logger.error('An OperationalError occurred')


def check_for_presence_in_db_and_code_check_entry(fam: str, name: str, patr: str, grp: str, var: str, git: str):
    """
    Функция, проверяющая, есть ли студент в БД и, если есть, проверяет его значение столбца res
    :return: None, если студента нет в БД и, если есть, значение столбца res определенного студента
    (True, если программа выполена верно и False, если не верно)
    """

    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    logger.info('The connection to the database was successful')
    cursor = connection.cursor()
    result = None
    try:
        cursor.callproc('code_check_entry', [f'{fam}', f'{name}', f'{patr}', f'{grp}', f'{var}',
                                             f'{git}'])
        result = cursor.fetchall()
        logger.info('The function worked successfully')
        return result[0][0]
    except OperationalError:
        logger.error('An OperationalError occurred')


def print_res():
    """
    Функция, осуществляющая вывод всех учеников
    :return: Возвращает всех учеников из БД, тип str
    """
    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    logger.info('The connection to the database was successful')
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute('SELECT fam, name, patronymic, grp, var, git FROM students')
        result = cursor.fetchall()
        total = []
        for user in result:
            user = list(user)
            total1 = []
            for val in user:
                total1.append(val.strip())
            total.append(total1[:-1])
        logger.info('The function worked successfully')
        result = ''
        for value in total:
            result += ' '.join(value) + "\n"
        return result
    except OperationalError:
        logger.error('An OperationalError occurred')
