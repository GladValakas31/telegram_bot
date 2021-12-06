import telebot
from student_func import registration
from database import print_res
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def get_information(message):
    bot.send_message(message.chat.id, """
    Пришли мне своё ФИО, номер группы (буквенно-циферно), номер варианта (числом) и ссылку github'а со своим заданием 
    в формате: 'Петров Петр Петрович 346Б 2 https://github.com/Your_name/Your_rep'
    """)

@bot.message_handler(commands=['database'])
def database(message):
    bot.send_message(message.chat.id, print_res())

@bot.message_handler(content_types=['text'])
def student_register(message):
    registration(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
