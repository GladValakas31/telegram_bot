import telebot
from database import execute_query, check_for_presence_in_db_and_code_check_entry
from gitnub_func import check_student_program
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


def registration(message):
    """
    Функция, осуществляющая проверку правильности введенных данных учеником;
    Проверяет программу ученика на правильность, записывает ученика с результатом проверки его программы в БД
    """

    # Проверка на правильность ввода данных
    info = message.text.split()
    if len(info) != 6:
        return bot.send_message(message.chat.id, 'Нехватка ваших данных')
    try:
        fam, name, patr, grp, var, git = info[0].capitalize(), info[1].capitalize(), info[2].capitalize(), info[3], \
                                         int(info[4]), info[5]
    except ValueError:
        return bot.send_message(message.chat.id, 'Некорректная информация')
    for value in (name, fam, patr):
        for letter in value:
            if not letter.isalpha():
                return bot.send_message(message.chat.id, 'Некорректное ФИО')
    groups = ('312Б', '321Б', '314Б')
    if grp not in groups:
        return bot.send_message(message.chat.id, 'Некорректная группа')
    if var < 0 or var > 10:
        return bot.send_message(message.chat.id, 'Некорректный номер варианта (вариант должен быть от 1 до 9)')
    if 'https://github.com/' not in git:
        return bot.send_message(message.chat.id, 'Некорректная ссылка')

    # Вызов функций базы данных и проверки программы студента
    var = str(var)
    if check_for_presence_in_db_and_code_check_entry(fam, name, patr, grp, var, git) is None:
        if check_student_program(git):
            execute_query(
                f"SELECT data_recording('{fam}', '{name}', '{patr}', '{grp}', '{var}', '{git}');")
            return bot.send_message(message.chat.id, 'Ваша программа прошла проверку, вы записаны в БД')
        else:
            res = False
            execute_query(
                f"SELECT data_recording('{fam}', '{name}', '{patr}', '{grp}', '{var}', '{git}', '{res}');")
            return bot.send_message(message.chat.id, 'Ваша программа не прошла проверку, вы записаны в БД')
    elif check_for_presence_in_db_and_code_check_entry(fam, name, patr, grp, var, git) is False:
        if not check_student_program(git):
            return bot.send_message(message.chat.id,
                                    'Ваша программа снова не прошла проверку (вы уже были записаны в БД)')
        else:
            execute_query(f"SELECT update_student_result('{fam}', '{name}', '{patr}', '{grp}', '{var}', '{git}');")
            return bot.send_message(message.chat.id,
                                    'Ваша программа прошла проверку, ваши данные перезаписаны в БД')
    else:
        return bot.send_message(message.chat.id,
                                'Ваша программа уже была проверена и прошла проверку, также вы уже были записаны в БД')
