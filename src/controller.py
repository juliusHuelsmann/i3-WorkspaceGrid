#!/bin/python3


import sys
import os
from grid import GridInterface
import time
sys.path.append(os.path.realpath(__file__))
import pyinotify

class Controller(pyinotify.ProcessEvent):
    """
    This controller class is used for the productive version of i3grid, 
    like it works much quicker than the interface provided via i3GridInterface.

    This Controller runs as a daemon on startup and reacts upon notifications 
    via named pipes. 
    """

    def __init__(self):

        self.wm = pyinotify.WatchManager()
        self.notifier = pyinotify.Notifier(self.wm, self)
        self.worker = GridInterface()

    def watch(self):

        # path of the pipe 
        self.path = "/tmp/mypipe"
        open(self.path, 'w').close()

        pipe_fd = os.open(self.path, os.O_RDONLY | os.O_NONBLOCK)
        self.pipe = os.fdopen(pipe_fd)

        wdd = self.wm.add_watch(self.path, pyinotify.IN_MODIFY)
        self.notifier.loop()

    def process_IN_MODIFY(self, evt):
        """
        Hook on the named pipe, launches the command written into the pipe.
        """
        message = self.pipe.read()
        if len(message):
            message = message[:-1]

            if (message=="exit"):
                exit()

            message = "self.worker." + message + "()"
            self.worker.reloadWorkspaces()
            try:
                print(time.time() , "Executing message" + message + "!")
                exec(message)
            except:    
                print("error, did not understand " + message + " as command.")



handler = Controller()
handler.watch()





