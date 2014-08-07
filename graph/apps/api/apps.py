__author__ = 'arun'

from django.apps import AppConfig
from django.conf import settings

import signal
import subprocess
import os

ipython_process = None
run_once = False

def handle_kill_server(signal, frame):
    global ipython_process
    if ipython_process:
        print "Killing ipython notebook"
        ipython_process.terminate()
        ipython_process = None

class ApiConfig(AppConfig):
    name = "graph.apps.api"
    verbose_name = "Graph API"

    def ready(self):
        global ipython_process, run_once
        print "existing process: ", ipython_process
        print "run once: ", run_once
        if run_once:
            return
        print "Starting ipython notebook"
        run_once = True
        NOTEBOOK_DIR = os.path.join(os.path.abspath(os.path.join(settings.PROJECT_DIR, os.pardir)), 'notebooks')
        ipython_process = subprocess.Popen(['ipython','notebook','--pylab=inline'], cwd=NOTEBOOK_DIR)
        signal.signal(signal.SIGINT, handle_kill_server)