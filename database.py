# -*- coding: utf-8 -*-


def save_task(user, task_text):
    print "Save for %s this task: %s" % (user['username'], task_text)
    id = len(task_text)
    return id
    
    
def get_task(username, type, time):
    return "Go fuck yourself"