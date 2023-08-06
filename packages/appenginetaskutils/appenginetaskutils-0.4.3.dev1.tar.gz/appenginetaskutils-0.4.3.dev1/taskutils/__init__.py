from __future__ import absolute_import

TASKUTILS_LOGGING = False
TASKUTILS_DUMP = False

import taskutils.task as taskpy
from taskutils.task import task, addrouteforwebapp, addrouteforwebapp2, get_taskroute, set_taskroute
from taskutils.flaskutil import setuptasksforflask
from flask import Flask

def set_logging(value):
    global TASKUTILS_LOGGING
    TASKUTILS_LOGGING = value

def get_logging():
    global TASKUTILS_LOGGING
    return TASKUTILS_LOGGING or TASKUTILS_DUMP

def set_dump(value):
    global TASKUTILS_DUMP
    TASKUTILS_DUMP = value

def get_dump():
    global TASKUTILS_DUMP
    return TASKUTILS_DUMP

app = Flask(__name__)

setuptasksforflask(app)

