# -*- coding: utf-8 -*-
import sys
print "Encoding is", sys.stdin.encoding

time_list = [0, '15 минут', 'час', 'день']
location_list = [0, 'дом', 'дача', 'работа', 'комп']

def save_task(user, task_text):
    print "Save for %s this task: %s" % (user['username'], task_text)
    id = len(task_text)
    return id
    
    
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