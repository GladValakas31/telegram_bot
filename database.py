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
    UPDATE students
    SET res = True
    WHERE fam='...' AND name='...' AND patronymic='...' AND grp='...' AND var='...'AND git='...';
    Это запрос для обновления инф-ции в столбце res опеределенного студента
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



def check_for_presence_in_db(stud):
    """
    Функция, проверяющая, есть ли студент в БД.
    :param stud: это пермемнная вида: 'Имя Фамилия Отчество Группа Вариант Гитхаб'
    :return: True, если студент есть в БД и False, если его там нет или если БД пустая
    """

    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    logger.info('The connection to the database was successful')
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute('SELECT * FROM students')
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        total = []
        for user in result:
            user = list(user)
            total1 = []
            for val in user:
                if isinstance(val, bool):
                    continue
                total1.append(val.strip())
            total.append(total1)
        logger.info('The function worked successfully')
        for st in total:
            if ' '.join(st) == stud:
                return True
        return False
    except OperationalError:
        logger.error('An OperationalError occurred')





def data_recording(fam: str, name: str, patronymic: str, grp: str, var: str, git: str, res: bool) -> None:

    """Функция, осуществляющая запись ученика в БД, ничего не возвращает"""

    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    logger.info('The connection to the database was successful')
    insert_query = (f"INSERT INTO students (fam, name, patronymic, grp, var, git, res) VALUES ('{fam}', '{name}', '{patronymic}', '{grp}', '{var}', '{git}', {res})")

    cursor = connection.cursor()
    cursor.execute(insert_query)
    connection.commit()
    logger.info('The function worked successfully')


def code_check_entry(fam, name, patronymic, grp, var, git):

    """
    Функция, проверяющая значение столбца res у определенного студента
    :return: значение столбца res (True или False)
    """
    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute('SELECT * FROM students')
        result = cursor.fetchall()
        total = []
        for user in result:
            user = list(user)
            total1 = []
            for val in user:
                if isinstance(val, bool):
                    total1.append(val)
                else:
                    total1.append(val.strip())
            total.append(total1)
        logger.info('The function worked successfully')
        for stud in total:
            if stud[0] == fam and stud[1] == name and stud[2] == patronymic and stud[3] == grp and stud[4] == var and stud[5] == git:
                return stud[6]
    except OperationalError:
        logger.error('An OperationalError occurred')


def print_res():
    """
    Функция, осуществляющая вывод всех учеников
    :return: Возвращает всех учеников из БД
    """
    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    logger.info('The connection to the database was successful')
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute('SELECT * FROM students')
        result = cursor.fetchall()
        total = []
        for user in result:
            user = list(user)
            total1 = []
            for val in user:
                if isinstance(val, bool):
                    continue
                else:
                    total1.append(val.strip())
            total.append(total1[:-1])
        logger.info('The function worked successfully')
        result = ''
        for value in total:
            result += ' '.join(value) + "\n"
        return result
    except OperationalError:
        logger.error('An OperationalError occurred')
