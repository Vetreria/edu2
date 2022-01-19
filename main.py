import telegram
from os import listdir
import os.path
import dotenv
import time
import argparse


def return_parser():
    delay_time = argparse.ArgumentParser()
    delay_time.add_argument("-t", "--time", type=int, default=86400)
    return delay_time


def send_list_photo(bot, user_time, tg_chat):
    for image in listdir("images"):
        with open("images/{}".format(image), "rb") as f:
            bot.send_photo(chat_id=tg_chat, photo=f)
        time.sleep(user_time)


def main():
    pause = return_parser()
    namespace = pause.parse_args()
    user_time = namespace.time
    dotenv.load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    tg_chat = os.getenv("TG_CHAT")
    bot = telegram.Bot(token=tg_token)
    send_list_photo(bot, user_time, tg_chat)


if __name__ == "__main__":
    main()
