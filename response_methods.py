# -*- coding: utf-8 -*-
from database import save_task, show_tasks, get_task, update_task, get_time, get_location
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import ast


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Привет, любой текст который ты пришлёшь я сохраню как задачу!")
    


def show(bot, update):
    tasks = show_tasks(update.message.from_user)
    query = update.callback_query

    bot.sendMessage(chat_id=update.message.chat_id, text="Задачи:  %s" % tasks)
    


def get_task(bot, update):
    id = save_task(update.message.from_user, update.message.text)
    def create_time_button(num):
        return InlineKeyboardButton(get_time(num), callback_data="{'id':%s, 'time':%s}" % (id, num))
    keyboard = [[create_time_button(i) for i in range(1, 4)]]

                #[InlineKeyboardButton("Дом", callback_data='3')]]
                
    reply_markup = InlineKeyboardMarkup(keyboard)
                
    bot.sendMessage(chat_id=update.message.chat_id, text="Как думаешь, сколько времени это займёт?", reply_markup=reply_markup)
    
    
    
def button(bot, update):
    query = update.callback_query
    
    
    reply = ast.literal_eval(query.data)
    if 'time' in reply:
        bot.editMessageText(text="Ок, %s" % get_time(reply['time']),
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
        update_task(query.message.from_user, reply['id'], time=reply['time'])
                        
        def create_location_button(num):
            return InlineKeyboardButton(get_location(num), callback_data="{'id':%s, 'location':%s}" % (reply['id'], num))
            
        keyboard = [[create_location_button(i) for i in range(1, 5)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
            
        bot.sendMessage(chat_id=query.message.chat_id, text="Это где?", reply_markup=reply_markup)
        
    if 'location' in reply:
        bot.editMessageText(text="Ок, %s" % get_location(reply['location']),
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
        update_task(query.message.from_user, reply['id'], location=reply['location'])
    
    
