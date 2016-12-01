# -*- coding: utf-8 -*-
import logging
import json
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

def get_token():
    with open('private/token.txt') as token_file:
        result = token_file.read()
        print result
    return result

TOKEN = get_token()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)



def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Привет, любой текст который ты пришлёшь я сохраню как задачу!")

def get_task(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
get_task_handler = MessageHandler(Filters.text, get_task)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(get_task_handler)


updater.start_polling()


