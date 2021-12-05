import psycopg2
from psycopg2 import OperationalError


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



def execute_query(connection, query):
    """
    Функция, осуществляющая введение запроса в БД через переменную query.

    UPDATE students
    SET res = True
    WHERE fam='...' AND name='...' AND patronymic='...' AND grp='...' AND var='...'AND git='...';
    Это запрос для обновления инф-ции в столбце res опеределенного студента

    :param connection: подключение к БД
    :param query: запрос в PostrgeSQL
    :return: None
    """
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Запрос query выполнено успешно")
    except OperationalError:
        print("Произошла ошибка 'OperationalError'")



def check_for_presence_in_db(connection, stud):
    """
    Функция, проверяющая, есть ли студент в БД.
    :param connection: подключение к БД
    :param stud: это пермемнная вида: 'Имя Фамилия Отчество Группа Вариант, Гитхаб'
    :return: True, если студент есть в БД и False, если его там нет или если БД пустая
    """

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
        for st in total:
            if ' '.join(st) == stud:
                return True
        return False
    except OperationalError:
        print("Произошла ошибка OperationalError")



def data_recording(connection, fam: str, name: str, patronymic: str, grp: str, var: str, git: str, res: bool) -> None:

    """Функция, осуществляющая запись ученика в БД, ничего не возвращает"""

    create_connection("student", "postgres", "89377366098v", "127.0.0.1", "5432")
    insert_query = (f"INSERT INTO students (fam, name, patronymic, grp, var, git, res) VALUES ('{fam}', '{name}', '{patronymic}', '{grp}', '{var}', '{git}', {res})")

    cursor = connection.cursor()
    cursor.execute(insert_query)
    connection.commit()



def code_check_entry(connection, fam, name, patronymic, grp, var, git):

    """
    Функция, проверяющая значение столбца res у определенного студента
    :return: значение столбца res (True или False)
    """

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
        for stud in total:
            if stud[0] == fam and stud[1] == name and stud[2] == patronymic and stud[3] == grp and stud[4] == var and stud[5] == git:
                return stud[6]
    except OperationalError:
        print("Произошла ошибка OperationalError")



def print_res():
    """
    Функция, осуществляющая вывод всех учеников
    :param connection: Подключение к БД
    :return: Возвращает всех учеников из БД
    """
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
        result = ''
        for value in total:
            result += ' '.join(value) + "\n"
        return result
    except OperationalError:
        print("Произошла ошибка OperationalError")

