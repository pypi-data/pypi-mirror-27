from getdone import GetDone as gd
from getdone.Task import Task
import sys


def main():
    # First argument is the name of the script file. So, ignoring it.
    default, args = sys.argv[0], sys.argv[1:]
    if len(args) == 0:
        gd.display_tasks()
    else:
        title = " ".join(args)
        gd.save_task(Task(title))