#!/usr/bin/env python3

import json
from enum import Enum

class Status(Enum):
    Ongoing = 1
    Completed = 2
    On_Hold = 3

tasklist = []
selected = None

def save():
    taskfile = json.dumps(tasklist,indent=2)

    try:
        with open("taskfile.json",'w') as f:
            f.write(taskfile) 
    except:
        print("There was a problem writing to file\n")

def load():
    global tasklist

    try:
        with open("taskfile.json",'r') as f:
            tasklist = json.loads(f.read()) 
    except:
        print("no file to load\n")

def addTask():
    #add item
    id = len(tasklist)+1
    tasklist.append({
        'id': f'{id}',
        'info': input("Enter Task: "),
        'status': 1
    })

    save()

def refreshTask():
    cur = 1
    for x in tasklist:
        x["id"] = f'{cur}'
        cur += 1
    save()

def deleteTask():
    global selected

    if selected is None:
        print('no task selected!!!\n')
    else:
        tasklist.pop(int(selected) - 1)
        refreshTask()
        selected = None

def updateTask(action):
    global selected

    if selected is None:
        print('no task selected!!!\n')
    else:
        cur = tasklist[int(selected) - 1 ]['status']

        if action == 'm':
            print('select status \nOngoing : 1\tCompleted : 2\tOn Hold : 3\n')
            ans = input("*> ")
            match (ans):
                case ('1'|'2'|'3'):
                    tasklist[int(selected) - 1 ]['status'] = int(ans)
                case (_):
                    print("invalid option\n")
                    return
            ##toggle update##
            # tasklist[int(selected) - 1 ]['status'] = max(1,(cur+1)%4)
        elif action == 'e':
            ans = input(f"edit*{selected}*> ")
            tasklist[int(selected) - 1 ]['info'] = ans

        save()
        selected = None

def listTask():
    load()

    #Header
    print("-"*101)
    print(f"|{'ID':<3}|{'TASK':^75}|{'status':^20}|")
    print("-"*101)
    ##
    
    for item in tasklist:
        try:
             print(f"|{item["id"]:3}|{item["info"]:75}|{Status(item["status"]).name:^20}|")
        except:
            print('there was a problem loading task....')

    #footer
    print("-"*101)

def helpMenu():
    print('''
    commands:
    l \t list all tasks
    c \t create new task
    s \t select a task
    d \t delete selected task **A task most be selected**
    e \t edit selected task **A task most be selected**
    m \t mark a task as <ongoing|completed|on hold> **A task most be selected**
    q \t quit\n
    ''')

##Execution start
listTask()
active=True

while active:

    #Don't mind the nested format string :)
    response = input(f'{ f"({selected})" if selected is not None else ''}> ')
    match (response):
        case ('l'):
            listTask()
#            print(tasklist['task1']['id'])
#            print(type(tasklist['task1']['id']))
        case ('q'):
            active = False 
            print('exiting...\n')
        case ('h'):
            helpMenu()
        case ('c'):
            addTask()
        case ('e'):
            updateTask('e')
        case ('s'):
            print('select a task by id \n')
            ans = input('@ ')
            if int(ans) in range(1,len(tasklist)+1) and len(tasklist) > 0:
                selected = ans
            elif len(tasklist)==0:
                print('\ntasks are empty\n')
            else:
                print(f'task {ans} does not exist\n')
        case ('d'):
            deleteTask()
        case ('m'):
            updateTask('m')
        case (_):
            print('invalid option \n\nuse h to list commands.')
            pass