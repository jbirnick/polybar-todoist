import subprocess
import datetime
import todoist
import time

def api_token():
    return subprocess.run(['secret-tool','lookup','uuid','todoist_api_token'], capture_output=True, text=True).stdout


def filter_dueToday(item):
    if item['checked']: return False;
    if item['due'] == None: return False;

    duedate = datetime.datetime.strptime(item['due']['date'][0:10],'%Y-%m-%d').date()

    return duedate == datetime.date.today()


def countTasks(items):
    count = {1: 0, 2: 0, 3: 0, 4: 0}
    for item in items:
        count[item['priority']] += 1
    return count


api = todoist.TodoistAPI(api_token())

while True:
    try:
        api.sync()
        count = countTasks(api.items.all(filt=filter_dueToday))
        print('%{{B#de4c4a}} {0[4]} %{{B-}}%{{B#f49c18}} {0[3]} %{{B-}}%{{B#4073d6}} {0[2]} %{{B-}}%{{B#444444}} {0[1]} %{{B-}}'.format(count))
    except:
        print(' ERROR ')
    time.sleep(10)
