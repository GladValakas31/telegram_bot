# 1) Подключаем БД
# 2) Проверяем наличие студента в БД
# 3.1) Если студента нет в БД:
#     3.1.1) Проверяем его программу.
#         Если она выполнена верно:
#             3.1.1.1) Заносим его в БД с записью в столбец res: True
#         Если работа выполнена неверно:
#             3.1.1.2) Заносим его в БД с записью в столбец res: False
# 3.2) Если студент есть в БД:
#     Если в столбце res запись False:
#         3.2.1) Проверяем его программу снова
#             Если программа неверная опять:
#                 3.2.1.1) Ничего не делаем
#             Если программа верная:
#                 3.2.1.2) Меняем запись в таблице res в БД на True
#     Если в столбце res запись True:
#         3.2.2) Ничего не делаем


import telebot
from database import execute_query, check_for_presence_in_db, data_recording, code_check_entry
from gitnub_func import check_student_program
bot = telebot.TeleBot('') # введите свое значение токена телеграм бота

def registration(message):
    """
    Функция, осуществляющая проверку правильности введенных данных учеником;
    Проверяет программу ученика на правильность, записывает ученика с результатом проверки его программы в БД
    """

    info = message.text.split()
    if len(info) != 6:
        return bot.send_message(message.chat.id, 'Нехватка ваших данных')
    try:
        fam, name, patr, grp, var, git = info[0].capitalize(), info[1].capitalize(), info[2].capitalize(), info[3], int(info[4]), info[5]
    except ValueError:
        return bot.send_message(message.chat.id, 'Некорректная информация')
    for value in (name, fam, patr):
        for letter in value:
            if letter in """0123456789.+/*-,:;'"`!@#$%^&()=/|{}<>?""":
                return bot.send_message(message.chat.id, 'Некорректное ФИО')
    groups = ('312Б', '321Б', '314Б')
    if grp not in groups:
        return bot.send_message(message.chat.id, 'Некорректная группа')
    if var < 0 or var > 10:
        return bot.send_message(message.chat.id, 'Некорректный номер варианта (вариант должен быть от 1 до 9)')
    if 'https://github.com/' not in git:
        return bot.send_message(message.chat.id, 'Некорректная ссылка')

    info1 = f'{fam} {name} {patr} {grp} {var} {git}'
    var = str(var)
    if not check_for_presence_in_db(info1):
        if check_student_program(git):
            res = True
            data_recording(fam, name, patr, grp, var, git, res)
            return bot.send_message(message.chat.id, 'Ваша программа прошла проверку, вы записаны в БД')
        else:
            res = False
            data_recording(fam, name, patr, grp, var, git, res)
            return bot.send_message(message.chat.id, 'Ваша программа не прошла проверку, вы записаны в БД')
    else:
        if not code_check_entry(fam, name, patr, grp, var, git):
            if not check_student_program(git):
                return bot.send_message(message.chat.id, 'Ваша программа снова не прошла проверку (вы уже были записаны в БД)')
            else:
                query = f"""UPDATE students SET res = True WHERE fam='{fam}' AND name='{name}' AND patronymic='{patr}' AND grp='{grp}' AND var='{var}' AND git='{git}';"""
                execute_query(query)
                return bot.send_message(message.chat.id, 'Ваша программа прошла проверку, ваши данные перезаписаны в БД')
        else:
            return bot.send_message(message.chat.id,'Ваша программа уже была проверена и прошла проверку, также вы уже были записаны в БД')
