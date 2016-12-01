# -*- coding: utf-8 -*-
from database import save_task, get_task
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Привет, любой текст который ты пришлёшь я сохраню как задачу!")
    

def get_task(bot, update):
    id = save_task(update.message.from_user, update.message.text)
    keyboard = [[InlineKeyboardButton("15 мин", callback_data='{id:%s, time:%s}' % (id, 1)),
                 InlineKeyboardButton("час", callback_data='{id:%s, time:%s}' % (id, 2)),
                 InlineKeyboardButton("день", callback_data='{id:%s, time:%s}' % (id, 3))],

                [InlineKeyboardButton("Дом", callback_data='3')]]
                
    reply_markup = InlineKeyboardMarkup(keyboard)
                
    bot.sendMessage(chat_id=update.message.chat_id, text="Как думаешь, сколько времени это займёт?", reply_markup=reply_markup)
    
    
def button(bot, update):
    query = update.callback_query

    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
    
    