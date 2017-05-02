# -*- coding: utf-8 -*-
from database import setup_logger, save_task, show_tasks, get_active_tasks, get_task_from_db, update_task, get_time, get_location, delete_task
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import ast

req_logger = setup_logger('req_logger', u'logs/req.log')


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Ты знаешь, что делать")
    keyboard = [[KeyboardButton(u'!Задачи в работе!'), KeyboardButton(u'!Получить задачу!')]] 
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    bot.sendMessage(chat_id=update.message.chat_id, text="Выбирай", reply_markup=reply_markup)


def get_task(bot, update):
    req_logger.info(u'Get task')
    query = update.callback_query

    def create_show_button(t, l):
        if not t:
            label = "%s" % get_location(l)
        else:
            label = get_time(t)
        return InlineKeyboardButton(label, callback_data="{'action':'show', 'time':%d, 'location': %d}" % (t, l))
    # keyboard = [[create_time_button(i) for i in range(1, 4)]]
    keyboard = []
    for j in range(1, 5):
        time_str = [create_show_button(i, j) for i in range(0, 4)]
        keyboard.append(time_str)

          
    reply_markup = InlineKeyboardMarkup(keyboard)
                
    bot.sendMessage(chat_id=update.message.chat_id, text="Какие задачи показать??", reply_markup=reply_markup)



def get_active_task(bot, update):
    req_logger.info(u'get_active_task')
    bot.sendMessage(chat_id=update.message.chat_id, text="Вот задачи которые ты якобы делаешь:")
    active_tasks = get_active_tasks(update.message.from_user)
    for t in active_tasks:
        keyboard=[[InlineKeyboardButton('Не делаю!', callback_data="{'action':'update', 'id':%s, 'status':0}" %  t[0]),
            InlineKeyboardButton('Сделал!', callback_data="{'action':'delete', 'id':%s}" % t[0])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=update.message.chat_id, text=t[1], reply_markup=reply_markup)
    

def add_task(bot, update):
    print "ADD TASK"
    req_logger.info(u'Add_task')
    id = save_task(update.message.from_user, update.message.text)
    def create_time_button(num):
        return InlineKeyboardButton(get_time(num), callback_data="{'action':'update', 'id':%s, 'time':%s}" % (id, num))
    keyboard = [[create_time_button(i) for i in range(1, 4)]]
                
    reply_markup = InlineKeyboardMarkup(keyboard)
                
    bot.sendMessage(chat_id=update.message.chat_id, text="Как думаешь, сколько времени это займёт?", reply_markup=reply_markup)
    
    
    
def button(bot, update):
    query = update.callback_query
    
    reply = ast.literal_eval(query.data)
    print 'BUTTON:', reply
    if reply.get('action') == 'update':
        update_task(query.from_user, reply)
        if 'time' in reply:
            bot.editMessageText(text="Ок, %s" % get_time(reply['time']).encode('utf8'),
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id)
                            
            def create_location_button(num):
                return InlineKeyboardButton(get_location(num), callback_data="{'action':'update', 'id':%s, 'location':%s}" % (reply['id'], num))
                
            keyboard = [[create_location_button(i) for i in range(1, 5)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
                
            bot.sendMessage(chat_id=query.message.chat_id, text="Это где?", reply_markup=reply_markup)
            
        if 'location' in reply:
            bot.editMessageText(text="Ок, %s" % get_location(reply['location']).encode('utf8'),
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id)
    
    if reply.get('action') == 'show':
        
        number_of_tasks, task_id, task = get_task_from_db(query.from_user, reply.get('time', 0), reply.get('location', 0), reply.get('number', 0))
        reply['number'] = reply.get('number', 0) + 1
        if number_of_tasks == 0:
            bot.sendMessage(chat_id=query.message.chat_id, text='Таких нет!')
            return
        if reply['number'] >= number_of_tasks:
            reply['number'] = 0
            button_name = 'Давай сначала!'
        else:
            button_name = 'Следущую!'
        keyboard=[[InlineKeyboardButton('Делаю!', callback_data="{'action':'update', 'id':%s, 'status':1}" %  task_id),
        InlineKeyboardButton(button_name, callback_data=str(reply)),
        InlineKeyboardButton('Удалить!', callback_data="{'action':'delete', 'id':%s}" % task_id)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=query.message.chat_id, text=task, reply_markup=reply_markup)
    
    if reply.get('action') == 'delete':
        
        delete_task(reply.get('id'))
