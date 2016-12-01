# -*- coding: utf-8 -*-
import logging
import json
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters


from response_methods import start, get_task, button

def get_token():
    with open('private/token.txt') as token_file:
        result = token_file.read()
        print result
    return result

TOKEN = get_token()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)



updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
get_task_handler = MessageHandler(Filters.text, get_task)
button_handler = CallbackQueryHandler(button)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(get_task_handler)
dispatcher.add_handler(button_handler)


updater.start_polling()




