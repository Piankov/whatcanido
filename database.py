# -*- coding: utf-8 -*-
import sys
import MySQLdb
import MySQLdb.cursors


print "Encoding is", sys.stdin.encoding

time_list = [0, '15 минут', 'час', 'день']
location_list = [0, 'дом', 'дача', 'работа', 'комп']


db = MySQLdb.connect (
    host='localhost',
    user='root',
    passwd='root123',
    db='whatcanido',
    cursorclass = MySQLdb.cursors.DictCursor,
)
cur = db.cursor()


def get_user_id(username):
    return 5

def parse_responce(cur):
    rowDump = []
    for row in cur:
        rowDump.append(row)
    return rowDump


def get_last_id():
    query = 'SELECT LAST_INSERT_ID() as ID'
    cur.execute(query)
    id = parse_responce(cur)[0]['ID']
    return id


def save_task(user, task_text):
    user_id = get_user_id(user)
    query = 'INSERT INTO \
Tasks (Description, UserID) \
VALUES ("%s", %d)' % (task_text, user_id)
    print query

    cur.execute(query)
    db.commit()
    
    id = get_last_id() 

    print "Save for %s task(%d): %s" % (user['username'], id, task_text)
    return id


def show_tasks(user):
    user_id = get_user_id(user)
    query = 'SELECT * FROM Tasks \
WHERE UserID = %d' % user_id
    cur.execute(query)
    tasks = parse_responce(cur)
    
    return str(tasks)

    
    
def update_task(user, id, location = 0, time = 0):
    if time:
        print "Change time for user %s, task %d, to %s" % (user, id, get_time(time))
    if location:
        print "Change location for user %s, task %d, to %s" % (user, id, get_location(location))
 
 
def get_task(username, type, time):
    return "Go fuck yourself"
    

    
def get_time(n):
    return time_list[n]
    
def get_location(n):
    return location_list[n]
