from communication import Communicator
import telebot
import time
from multiprocessing.context import Process
import schedule


token = "5877520912:AAHK5suv6GXYotrLI5vNA9LwCVydV4np40E"
bot = telebot.TeleBot(token)
communicator = Communicator()


@bot.message_handler(content_types=['text'])
def bot_poll(msg):
    id, repl, markup = communicator.read_msg(msg)
    if markup:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        if markup == ['-']:
            keyboard = telebot.types.ReplyKeyboardRemove()
        else:
            for i in markup:
                keyboard.add(telebot.types.KeyboardButton(text=i))
        if len(repl) == 2:
            bot.send_document(id, repl[0], reply_markup=keyboard)
            return
        bot.send_message(id, repl, reply_markup=keyboard)
        return
    bot.send_message(id, repl)


def send_message1():
    list, msg = communicator.send_all_teachers()
    for i in list:
        bot.send_message(i, msg)


def send_message2():
    list, msg = communicator.send_all_admins()
    for i in list:
        bot.send_document(i, msg)

def f():
    communicator.clear_all_msgs()

schedule.every().day.at("00:00").do(f)
schedule.every().day.at("08:10").do(send_message1)
schedule.every().day.at("20:57").do(send_message2)

class ScheduleMessage():
    @staticmethod
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    @staticmethod
    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()

if __name__ == "__main__":
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)