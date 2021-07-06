#TODO use logger instead of this clusterfuck
import os.path
from datetime import datetime as dt

def log_this(data, filename):
    data = str(data)
    with open(os.path.join("app/logs/", filename), 'a') as logfile:
        logfile.write(dt.strftime(dt.now(),"%y-%m-%d %H:%M:%S") + "\n")
        if type(data) == str:
            logfile.write(data + "\n\n")
        # if type(data) == dict:
        #     for key in data:
        #         logfile.write(key + ": " + data[key] + "\n")
        # if type(data) == bool:
        #     logfile.write(str(data) + "\n")
        # if type(data) == int:
        #     logfile.write(str(data) + "\n")
        
    return True