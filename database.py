# -*- coding: utf-8 -*-
import sys
import MySQLdb
import MySQLdb.cursors
import logging


logging.basicConfig(format = u'[%(asctime)s] %(message)s', level = logging.INFO, filename = u'logs/database.log')


print "Encoding is", sys.stdin.encoding

time_list = [u'ВСЕГДА', u'15 минут', u'час', u'день']
location_list = [u'ВЕЗДЕ', u'дом', u'дача', u'работа', u'комп']


db = MySQLdb.connect (
    host='localhost',
    user='root',
    passwd='root123',
    db='whatcanido',
    charset="utf8",
    use_unicode=True,
    cursorclass = MySQLdb.cursors.DictCursor,
)
cur = db.cursor()


def execute_query(query):
    logging.info( u'QUERY: %s' % query)
    cur.execute(query)


def parse_responce(cur):
    rowDump = []
    for row in cur:
        rowDump.append(row)
    return rowDump


def get_user_id(username):
    execute_query("SELECT * FROM Users WHERE Login = '%s_%d'" % (username['username'], username['id']))
    user_id_list = parse_responce(cur)
    if user_id_list:
        logging.info( u'Get user id %d for user %s' % (user_id_list[0]['ID'], username))
        return user_id_list[0]['ID']
    
    execute_query('INSERT INTO \
Users (Login) \
VALUES ("%s_%d")' % (username['username'], username['id']))
    db.commit()
    new_id = int(get_last_id())
    logging.info( u'Add user with id %d for username %s' % (new_id, username))
    return new_id


def get_last_id():
    execute_query('SELECT LAST_INSERT_ID() as ID')
    id = parse_responce(cur)[0]['ID']
    return id


def save_task(user, task_text):
    user_id = get_user_id(user)
    execute_query('INSERT INTO \
Tasks (Description, UserID) \
VALUES ("%s", %d)' % (task_text, user_id))
    db.commit()
    id = get_last_id() 

    logging.info( u'Save task %d for user %s: %s' % (id, user['username'], task_text))
    return id


def show_tasks(user):
    user_id = get_user_id(user)
    execute_query('SELECT * FROM Tasks \
WHERE UserID = %d' % user_id)
    tasks = parse_responce(cur)
    str_tasks = []
    for d in tasks:
        print d
        tmp_task = '%s\n Time: %s, Location: %s' % (d['Description'], time_list[d['Time']], location_list[d['Location']])
        if d['Favorite']:
            tmp_task = '* ' + tmp_task
            str_tasks = [tmp_task] + str_tasks
        else:
            str_tasks.append(tmp_task)
    tasks = '\n'.join(str_tasks)
    return tasks

    
    
def update_task(user, reply_dict):
    # if I'm going to update several columns at once I have to think about concatinations
    user_id = get_user_id(user)
    
    update_str = ''
    for k in reply_dict:
         if k == 'id' or k == 'action':
             continue
         update_str += '%s = %d' % (k[0].upper()+k[1:], reply_dict[k])
    execute_query("UPDATE Tasks SET %s WHERE ID = %d AND UserID = %d" % (update_str, reply_dict['id'], user_id))
    db.commit() 
 
def get_task_from_db(user, time, location, number=0):
    user_id = get_user_id(user)
    if time:
        time_str = 'AND Time = %d' % time
    else:
        time_str = ''
    if location:
        location_str = 'AND Location = %d' % location
    else:
        location_str = ''
    execute_query('SELECT * FROM Tasks \
WHERE UserID = %d %s %s' % (user_id, time_str, location_str))
    try:
        return len(parse_responce(cur)), parse_responce(cur)[number]['ID'], parse_responce(cur)[number]['Description']
    except IndexError:
        return 0, 0, 'Таких нету!'
        
    
def get_time(n):
    return time_list[n]
    
def get_location(n):
    return location_list[n]
