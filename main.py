import telegram
from pathlib import Path
from os import listdir
import os.path
from urllib.parse import urlparse
import dotenv
import time
import argparse
from telegram.ext import defaults


def set_time():
    pause = argparse.ArgumentParser()
    pause.add_argument('-t', '--time', type=int, default=86400)
    return pause


def bot_send_list_photo(bot, user_time):
    for image in listdir('images'):
        bot.send_photo(chat_id='@antonspacetest', photo=open('images/'+image, "rb"))
        time.sleep(user_time)
    print(listdir('images'))


def main():
    pause = set_time()
    namespace = pause.parse_args()
    user_time = namespace.time
    dotenv.load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    bot = telegram.Bot(token = tg_token)
    bot_send_list_photo(bot, user_time)


if __name__ == "__main__":
    main()
